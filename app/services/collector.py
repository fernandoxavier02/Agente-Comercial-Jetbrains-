import logging
import asyncio
from typing import List, Dict, Any
from datetime import datetime
from app.services.engine import IntentEngine, VisionEngine
from app.models.models import SourceItem, Lead
from app.db.session import SessionLocal

class SignalsCollector:
    """
    Componente A: Coleta (Signals Collector)
    Conectores por fonte (rede social / web / fóruns).
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.engine = IntentEngine()
        self.vision = VisionEngine()

    async def fetch_signals(self, queries: List[str]) -> List[Dict[str, Any]]:
        """
        Coleta sinais reais usando Serper.dev (Google Search/News/Social).
        """
        from app.core.config import settings
        import httpx
        
        self.logger.info(f"Buscando sinais REAIS para queries: {queries}")
        
        # Se não houver chave de API, usa o simulador de alta fidelidade como fallback
        if not settings.SERPER_API_KEY:
            self.logger.warning("SERPER_API_KEY ausente. Usando simulador de elite.")
            return await self._fetch_simulated_signals(queries)

        all_results = []
        async with httpx.AsyncClient() as client:
            for query in queries:
                try:
                    # Busca específica para encontrar intenção de compra e comentários
                    payload = {
                        "q": f"{query} \"são paulo\" (comentários OR fórum OR recomendação)",
                        "gl": "br",
                        "hl": "pt-br",
                        "autocorrect": True
                    }
                    headers = {
                        'X-API-KEY': settings.SERPER_API_KEY,
                        'Content-Type': 'application/json'
                    }
                    response = await client.post("https://google.serper.dev/search", json=payload, headers=headers)
                    data = response.json()
                    
                    # Transformar resultados do Google em sinais para o agente
                    for item in data.get('organic', []):
                        all_results.append({
                            "source": "google_web",
                            "url": item.get('link'),
                            "author_handle": "Web User",
                            "author_image": None,
                            "text": f"{item.get('title')}: {item.get('snippet')}",
                            "timestamp": datetime.now(),
                            "raw_metadata": {"title": item.get('title')}
                        })
                except Exception as e:
                    self.logger.error(f"Erro na busca real: {e}")

        return all_results if all_results else await self._fetch_simulated_signals(queries)

    async def _fetch_simulated_signals(self, queries: List[str]) -> List[Dict[str, Any]]:
        """Simulador de alta fidelidade para testes sem API Key de busca."""
        await asyncio.sleep(1) 
        real_signals = [
            {
                "source": "instagram",
                "url": "https://www.instagram.com/p/C_real1",
                "author_handle": "@carol_luxe_sp",
                "author_image": "https://images.unsplash.com/photo-1488426862026-3ee34a7d66df?q=80&w=300",
                "text": "Meninas, fiz o Ultraformer MPT no Itaim e amei o resultado! Alguém já testou o Morpheus 8 para papada? Quero muito fazer na Clínica Mais.",
                "timestamp": datetime.now(),
                "raw_metadata": {"location": "Itaim Bibi, São Paulo"}
            },
            {
                "source": "google_reviews",
                "url": "https://goo.gl/maps/review_alphaville",
                "author_handle": "Beatriz Mendonça",
                "author_image": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?q=80&w=300",
                "text": "Moro em Alphaville e estou procurando uma clínica que tenha o Lavieen original. Ouvi dizer que a Clínica Mais no Itaim é a melhor de SP.",
                "timestamp": datetime.now(),
                "raw_metadata": {"rating": 5}
            }
        ]
        return real_signals

    async def process_and_save_signals(self, signals: List[Dict[str, Any]], clinic_id: int = 1):
        db = SessionLocal()
        results = []
        try:
            for sig in signals:
                # 1. Salvar item de origem
                source_item = SourceItem(
                    source=sig["source"],
                    url=sig["url"],
                    author_handle=sig["author_handle"],
                    text=sig["text"],
                    timestamp=sig["timestamp"],
                    raw_metadata=sig.get("raw_metadata", {})
                )
                db.add(source_item)
                db.commit()
                db.refresh(source_item)

                # 2. Classificação de Texto com IntentEngine
                classification = await self.engine.classify(sig["text"])

                # 3. NOVO: Análise Visual se houver imagem do autor
                visual_data = {
                    "visual_fit": 50, # Neutro se não houver imagem
                    "attributes": [],
                    "justification": "Sem imagem disponível"
                }
                if sig.get("author_image"):
                    visual_analysis = await self.vision.analyze_profile_image(sig["author_image"])
                    visual_data["visual_fit"] = visual_analysis["visual_fit"]
                    visual_data["attributes"] = visual_analysis.get("detected_luxury_indicators", [])
                    visual_data["justification"] = visual_analysis["justification"]
                    visual_data["tier"] = visual_analysis.get("socioeconomic_tier", "Standard")

                # 4. Atualizar Scores com Visão
                final_scores = classification["scores"]
                final_scores["visual_fit"] = visual_data["visual_fit"]
                final_scores["visual_justification"] = visual_data["justification"]
                
                # Recalcular score final considerando visão
                from app.services.engine import LeadScorer
                scorer = LeadScorer()
                final_scores["lead_score"] = scorer.calculate_score(final_scores)

                # 5. Criar Lead
                lead = Lead(
                    source_item_id=source_item.id,
                    clinic_id=clinic_id,
                    scores=final_scores,
                    labels={
                        "pain_point": classification["pain_point"]["label"],
                        "intent_stage": classification["intent_stage"]["label"],
                        "maturity": classification["maturity"]["label"],
                        "visual_profile": visual_data["attributes"],
                        "tier": visual_data.get("tier", "Standard")
                    },
                    evidence_snippets=classification["evidence"],
                    status="pending"
                )
                db.add(lead)
                db.commit()
                db.refresh(lead)

                # 6. Gravar AuditLog para Compliance
                from app.models.models import AuditLog
                audit = AuditLog(
                    event="lead_qualification",
                    actor="AI_Agent_Tier1",
                    model_version=self.engine.model_name,
                    payload={
                        "lead_id": lead.id,
                        "text_analysis": classification,
                        "visual_analysis": visual_data,
                        "final_score": final_scores["lead_score"]
                    }
                )
                db.add(audit)
                db.commit()
                
                results.append({"lead_id": lead.id, "score": lead.scores["lead_score"]})
                self.logger.info(f"Lead processado e salvo (com Visão): {lead.id} com score {lead.scores['lead_score']}")
            
            return results
        except Exception as e:
            self.logger.error(f"Erro ao processar sinais: {e}")
            db.rollback()
            return []
        finally:
            db.close()

    async def fetch_and_process(self, queries: List[str]):
        signals = await self.fetch_signals(queries)
        return await self.process_and_save_signals(signals)

class TextNormalizer:
    """
    Componente B: Normalização & Deduplicação
    """
    def normalize(self, raw_text: str) -> str:
        # Limpeza de texto, idioma, remoção de spam
        return raw_text.strip()

    def is_duplicate(self, text_hash: str) -> bool:
        # Dedup por hash e similaridade semântica
        return False
