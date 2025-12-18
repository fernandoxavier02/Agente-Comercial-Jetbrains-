import json
import logging
from typing import Dict, Any
from openai import OpenAI
from app.core.config import settings

class IntentEngine:
    """
    Componente C: Classificação (Intent Engine)
    Classifica dor estética, intenção, fit e risco.
    """
    def __init__(self, provider: str = None, model_name: str = None):
        self.provider = provider or settings.LLM_PROVIDER
        self.model_name = model_name or settings.LLM_MODEL
        self.logger = logging.getLogger(__name__)
        
        # Inicializar cliente baseado no provider
        if self.provider == "openai":
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        elif self.provider == "openrouter":
            self.client = OpenAI(
                base_url=settings.OPENROUTER_BASE_URL,
                api_key=settings.OPENROUTER_API_KEY,
            )
        elif self.provider == "ollama":
            self.client = OpenAI(
                base_url=settings.OLLAMA_BASE_URL,
                api_key="ollama", # Ollama geralmente não requer chave
            )
        else:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def classify(self, text: str) -> Dict[str, Any]:
        """
        Saída sempre estruturada (JSON) para parsing:
        labels, scores, evidences, risk_flags, strategy, drafts.
        """
        prompt = f"""
        VOCÊ É UM ANALISTA DE INTELIGÊNCIA SOCIAL E COMPORTAMENTAL DA 'CLÍNICA MÉDICA MAIS' EM SÃO PAULO.
        A Clínica Mais é uma clínica Tier 1 localizada no Itaim Bibi/Jardins, focada em Dermatologia, Estética Avançada e Longevidade.
        
        Sua tarefa é analisar o texto/comentário abaixo buscando leads para os seguintes serviços:
        - TECNOLOGIAS: Ultraformer MPT, Morpheus, Lavieen, Liftera.
        - INJETÁVEIS: Botox, Preenchimento (Ácido Hialurônico), Bioestimuladores (Sculptra, Radiesse).
        - PROTOCOLOS: Rejuvenescimento facial, contorno corporal, tratamento de manchas/melasma.

        CONDIÇÃO OBRIGATÓRIA: Identificar se o lead pertence à GRANDE SÃO PAULO.
        Bairros de Altíssima Prioridade (Elite): Itaim Bibi, Jardins, Vila Nova Conceição, Moema, Higienópolis, Pacaembu, Morumbi, Alto de Pinheiros.
        Cidades/Regiões de Alta Prioridade: Alphaville (Barueri/Santana de Parnaíba), Granja Viana, Santo André (Bairro Jardim), São Caetano do Sul.

        Texto: "{text}"
        
        ALÉM DO CONTEÚDO DIRETO, BUSQUE INDICADORES INDIRETOS:
        1. REFINAMENTO VOCABULAR: Uso de termos técnicos, elegância na escrita ou familiaridade com o universo premium.
        2. CÍRCULO SOCIAL/ASPIRACIONAL: Menção a locais, marcas ou estilos de vida que indicam que a pessoa pertence ou transita no alto padrão.
        3. MATURIDADE DE CONSUMO: A pessoa já consome procedimentos caros? Ela fala com propriedade sobre tecnologias (ex: Ultraformer, Morpheus, Bioestimuladores)?
        4. "DOG WHISTLES" DO LUXO: Expressões ou preocupações que apenas o público de alta renda possui (ex: manutenção de "quiet luxury", discrição, protocolos exclusivos).

        Retorne APENAS um JSON:
        {{
            "pain_point": {{"label": "queixa", "confidence": 0.0-1.0}},
            "intent_stage": {{"label": "estágio", "confidence": 0.0-1.0}},
            "maturity": {{"label": "experiência_no_luxo", "score": 0-100}},
            "is_sp_region": true/false (Grande São Paulo),
            "is_elite_neighborhood": true/false (Se pertence aos bairros de elite citados ou Alphaville),
            "detected_location": "nome da cidade ou bairro identificado",
            "scores": {{
                "fit": 0-100 (alinhamento com Clínica Mais e luxo),
                "intent": 0-100,
                "urgency": 0-100,
                "risk": 0-100,
                "social_status_signal": 0-100
            }},
            "subliminal_signals": ["lista de indícios indiretos de alto padrão"],
            "evidence": ["trechos que justificam"],
            "risk_flags": []
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "Você é um especialista em qualificação de leads para medicina estética."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            
            # Adicionar flags regionais aos scores para o Scorer
            result["scores"]["is_sp_region"] = result.get("is_sp_region", True)
            result["scores"]["is_elite_neighborhood"] = result.get("is_elite_neighborhood", False)
            
            # Calcular lead_score final usando o LeadScorer
            scorer = LeadScorer()
            result["scores"]["lead_score"] = scorer.calculate_score(result["scores"])
            
            return result
        except Exception as e:
            self.logger.error(f"Erro ao classificar com LLM: {e}")
            # Fallback para dados vazios em caso de erro
            return {
                "pain_point": {"label": "unknown", "confidence": 0.0},
                "intent_stage": {"label": "unknown", "confidence": 0.0},
                "maturity": {"label": "beginner", "score": 0},
                "scores": {"fit": 0, "intent": 0, "urgency": 0, "risk": 0, "lead_score": 0},
                "evidence": [],
                "risk_flags": ["error_in_classification"]
            }

class LeadScorer:
    """
    Componente E: Scoring & Priorização
    """
    def calculate_score(self, metrics: Dict[str, float]) -> float:
        # LeadScore ponderado para alto padrão (Prioriza Visual Fit, Luxury Signals e Social Signals)
        # w1*Fit + w2*Intent + w3*Urgency + w4*Maturity + w5*VisualFit + w6*SocialStatus - w7*Risk
        # Adicional: Penaliza se NÃO for da Grande São Paulo, Bônus para Bairros de Elite
        w = {
            "fit": 0.10, 
            "intent": 0.10, 
            "urgency": 0.05, 
            "maturity": 0.10, 
            "visual_fit": 0.35, # Perfil visual/posses
            "social_status": 0.20, # Sinais subliminares no texto
            "risk": 0.60 
        }
        
        # Geofencing: Grande São Paulo (Fator base)
        is_sp = metrics.get("is_sp_region", True)
        is_elite = metrics.get("is_elite_neighborhood", False)
        
        regional_multiplier = 1.0 if is_sp else 0.5 # Reduz o score pela metade se não for da Grande SP
        elite_bonus = 1.2 if is_elite else 1.0 # Bônus de 20% para bairros de elite (Itaim, Jardins, Alphaville)

        score = (
            w["fit"] * metrics.get("fit", 0) +
            w["intent"] * metrics.get("intent", 0) +
            w["urgency"] * metrics.get("urgency", 0) +
            w["maturity"] * metrics.get("maturity", 0) +
            w["visual_fit"] * metrics.get("visual_fit", 0) +
            w["social_status"] * metrics.get("social_status_signal", 0) -
            w["risk"] * metrics.get("risk", 0)
        )
        return max(0, min(100, score * regional_multiplier * elite_bonus))

class VisionEngine:
    """
    Componente G: Análise Visual (Vision Engine)
    Analisa imagens para identificar perfil socioeconômico e cuidado estético.
    """
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.model_name = settings.VISION_MODEL
        self.logger = logging.getLogger(__name__)
        
        if self.provider == "openrouter":
            self.client = OpenAI(
                base_url=settings.OPENROUTER_BASE_URL,
                api_key=settings.OPENROUTER_API_KEY,
            )
        else:
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def analyze_profile_image(self, image_url: str) -> Dict[str, Any]:
        prompt = """
        VOCÊ É UM INVESTIGADOR DE ELITE ESPECIALIZADO EM PATRIMÔNIO E ESTILO DE VIDA DE ALTO LUXO (UHNW - Ultra High Net Worth).
        Sua tarefa é realizar uma perícia detalhada na imagem para identificar sinais inequívocos de riqueza e alto poder aquisitivo.
        
        PERÍCIA DE ELEMENTOS (SEJA EXTREMAMENTE MINUCIOSO):
        
        1. OBJETOS DE ALTO VALOR (Possessions):
           - RELÓGIOS: Identifique se há presença de marcas como Rolex, Patek Philippe, Audemars Piguet, Cartier, Richard Mille.
           - JOIAS: Presença de diamantes, pedras preciosas, joalheria de marca (Tiffany, Bulgari, Van Cleef & Arpels).
           - BOLSAS/ACESSÓRIOS: Identifique modelos icônicos de luxo (Hermès Birkin/Kelly, Chanel Classic, Louis Vuitton, Gucci).
        
        2. LOGÍSTICA E MEIOS DE TRANSPORTE (Luxury Logistics):
           - AVIAÇÃO: Cabines de Primeira Classe ou Executiva, jatos particulares, salas VIP exclusivas.
           - NÁUTICA: Iates, lanchas de alto padrão, marinas exclusivas.
           - AUTOMÓVEIS: Interiores de carros de luxo (Porsche, Ferrari, Lamborghini, Rolls-Royce, Mercedes-Benz Classe S).
        
        3. CENÁRIOS E ESTILO DE VIDA (Elite Scenarios):
           - AMBIENTES: Resorts 5 estrelas, hotéis de luxo (Aman, Four Seasons, Rosewood), restaurantes com estrela Michelin.
           - EVENTOS: Áreas VIP, camarotes, eventos de gala, destinos de viagem internacionais exclusivos (Courchevel, St. Tropez, Dubai).
        
        4. APARÊNCIA "CUIDADA POR ESPECIALISTAS" (High-End Maintenance):
           - Estética impecável que sugere altos gastos mensais com procedimentos médicos, odontologia estética e hair care de luxo.
        
        Retorne um JSON de perícia técnica:
        {
            "visual_fit": 0-100 (Score agressivo: 100 apenas para luxo extremo),
            "asset_audit": {
                "high_value_objects": ["lista de objetos caros identificados"],
                "luxury_environment": "descrição do local (ex: classe executiva, iate, resort)",
                "brand_detection": ["marcas de grife identificadas no vestuário/acessórios"]
            },
            "socioeconomic_tier": "VIP, Platinum, Gold, ou Standard",
            "detected_luxury_indicators": ["lista de evidências de riqueza"],
            "justification": "Análise técnica do patrimônio visual estimado e por que esta pessoa é o alvo Tier 1 da clínica (tratamentos de alto ticket)."
        }
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": image_url}}
                        ],
                    }
                ],
                max_tokens=500,
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            self.logger.error(f"Erro na análise visual: {e}")
            return {
                "visual_fit": 50,
                "indicators": {"aesthetic_care": 50, "socioeconomic_signals": 50, "selfie_affinity": 50},
                "profile_tags": ["unknown"],
                "analysis_summary": "Não foi possível analisar a imagem."
            }
