import asyncio
from app.services.engine import IntentEngine

async def test_geofencing_expansion():
    print("--- Testando Expansão de Geofencing e Bairros de Elite ---")
    engine = IntentEngine()

    test_cases = [
        {
            "name": "Lead Elite SP (Itaim Bibi)",
            "text": "Moro no Itaim Bibi e quero fazer Ultraformer MPT na Clínica Mais.",
            "expected_region": True,
            "expected_elite": True
        },
        {
            "name": "Lead Grande SP (Alphaville)",
            "text": "Sou de Alphaville e gostaria de agendar uma avaliação para Morpheus e bioestimuladores.",
            "expected_region": True,
            "expected_elite": True
        },
        {
            "name": "Lead Grande SP (Santo André)",
            "text": "Moro em Santo André, vi o site de vocês. Vocês atendem Lavieen aos sábados?",
            "expected_region": True,
            "expected_elite": False
        },
        {
            "name": "Lead Fora de SP (Curitiba)",
            "text": "Oi, sou de Curitiba e vou viajar para SP mês que vem. Queria saber o preço do botox.",
            "expected_region": False,
            "expected_elite": False
        }
    ]

    for case in test_cases:
        print(f"\nTestando: {case['name']}")
        result = await engine.classify(case['text'])
        
        is_sp = result.get("is_sp_region")
        is_elite = result.get("is_elite_neighborhood")
        location = result.get("detected_location")
        score = result["scores"]["lead_score"]
        
        print(f"  Localização detectada: {location}")
        print(f"  Na Grande SP? {is_sp} (Esperado: {case['expected_region']})")
        print(f"  Bairro Elite? {is_elite} (Esperado: {case['expected_elite']})")
        print(f"  Lead Score Final: {score:.2f}")

        # Verificação básica
        if is_sp != case['expected_region']:
            print(f"  [AVISO] Região SP inconsistente!")
        if is_elite != case['expected_elite']:
            print(f"  [AVISO] Classificação Elite inconsistente!")

if __name__ == "__main__":
    asyncio.run(test_geofencing_expansion())
