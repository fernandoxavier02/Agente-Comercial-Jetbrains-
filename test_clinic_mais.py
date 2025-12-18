import asyncio
from app.services.engine import IntentEngine

async def test_clinic_mais_context():
    print("--- Testando Contexto Clínica Mais (São Paulo) ---")
    engine = IntentEngine()
    
    # Caso 1: Lead de SP com interesse em tecnologia da clínica
    text_sp = "Moro no Itaim e estou procurando onde fazer Ultraformer MPT, quero algo bem natural."
    print(f"\nTestando lead SP: '{text_sp}'")
    result_sp = await engine.classify(text_sp)
    print(f"É de SP? {result_sp.get('is_sp_region')}")
    print(f"Score: {result_sp['scores']['lead_score']}")
    print(f"Sinais: {result_sp.get('subliminal_signals')}")

    # Caso 2: Lead de fora de SP
    text_rj = "Alguém indica botox no Rio de Janeiro? Sou da Barra."
    print(f"\nTestando lead fora de SP: '{text_rj}'")
    result_rj = await engine.classify(text_rj)
    print(f"É de SP? {result_rj.get('is_sp_region')}")
    print(f"Score: {result_rj['scores']['lead_score']} (Deve ser menor devido à localização)")

    # Caso 3: Lead de luxo com termo técnico
    text_luxury = "Preciso de um protocolo de bioestimuladores (Sculptra) para manutenção, prefiro clínica discreta nos Jardins."
    print(f"\nTestando lead Luxo/SP: '{text_luxury}'")
    result_lux = await engine.classify(text_luxury)
    print(f"É de SP? {result_lux.get('is_sp_region')}")
    print(f"Score: {result_lux['scores']['lead_score']}")
    print(f"Maturidade: {result_lux.get('maturity')}")

if __name__ == "__main__":
    asyncio.run(test_clinic_mais_context())
