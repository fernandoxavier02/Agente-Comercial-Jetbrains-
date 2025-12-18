import asyncio
import logging
from app.services.collector import SignalsCollector
from app.db.session import SessionLocal
from app.models.models import Lead

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_capture_mission():
    print("\n--- 🚀 INICIANDO MISSÃO DE CAPTURA: ELITE SÃO PAULO ---")
    
    collector = SignalsCollector()
    
    # Keywords de Alto Padrão para a Clínica Mais
    queries = [
        "Ultraformer MPT",
        "Morpheus 8",
        "Lavieen",
        "Sculptra",
        "Radiesse",
        "Bioestimulador em SP",
        "Clínica no Itaim"
    ]
    
    logger.info(f"Buscando sinais para as tecnologias de elite: {queries}")
    
    # 1. Coletar
    signals = await collector.fetch_signals(queries)
    logger.info(f"Coletados {len(signals)} potenciais sinais.")
    
    # 2. Processar (IA + Visão + Geofencing + Scoring)
    # Isso já salva no banco de dados automaticamente
    results = await collector.process_and_save_signals(signals)
    
    # 3. Mostrar Resultados do Ranking
    print("\n--- 🏆 RANKING DE LEADS QUALIFICADOS (Tier 1 SP) ---")
    db = SessionLocal()
    try:
        # Buscar os leads salvos ordenados por score
        leads = db.query(Lead).order_by(Lead.scores['lead_score'].desc()).limit(10).all()
        
        for i, lead in enumerate(leads):
            score = lead.scores.get('lead_score', 0)
            tier = lead.labels.get('tier', 'Standard')
            location = lead.scores.get('detected_location', 'N/A')
            
            star = "💎 VIP" if score > 30 else "✅ Qualificado"
            
            print(f"{i+1}. [{star}] Score: {score:.2f} | Tier: {tier}")
            print(f"   Local: {location}")
            print(f"   Queixa: {lead.labels.get('pain_point')}")
            print(f"   Contexto Visual: {lead.scores.get('visual_justification', 'Sem imagem')[:100]}...")
            print("-" * 50)
            
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(run_capture_mission())
