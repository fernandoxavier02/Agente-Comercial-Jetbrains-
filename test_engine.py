import asyncio
import os
from app.services.engine import IntentEngine
from dotenv import load_dotenv

load_dotenv()

async def test_intent_engine():
    engine = IntentEngine()
    
    test_texts = [
        "Estou com umas manchas escuras no rosto que me incomodam muito. Já usei vários cremes e nada resolve.",
        "Quanto custa o preenchimento labial? Quero fazer amanhã!",
        "Vi um vídeo sobre botox e fiquei curiosa, mas tenho medo de ficar artificial."
    ]
    
    for text in test_texts:
        print(f"\n--- Analisando: {text[:50]}... ---")
        result = await engine.classify(text)
        print(f"Dor: {result['pain_point']['label']} (Conf: {result['pain_point']['confidence']})")
        print(f"Estágio: {result['intent_stage']['label']}")
        print(f"Lead Score: {result['scores']['lead_score']}")
        print(f"Evidências: {result['evidence']}")
        if result['risk_flags']:
            print(f"Alertas: {result['risk_flags']}")

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("AVISO: OPENAI_API_KEY não configurada no ambiente. O teste falhará ou usará o fallback.")
    asyncio.run(test_intent_engine())
