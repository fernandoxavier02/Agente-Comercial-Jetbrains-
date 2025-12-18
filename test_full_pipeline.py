import asyncio
import logging
from app.services.collector import SignalsCollector

# Configurar logging para ver os resultados no console
logging.basicConfig(level=logging.INFO)

async def test_full_pipeline():
    print("\n=== Iniciando Teste de Fluxo Completo (End-to-End) ===\n")
    
    collector = SignalsCollector()
    
    # 1. Coletar Sinais (Mock)
    print("Passo 1: Coletando sinais...")
    signals = await collector.fetch_signals(queries=["melasma", "botox"])
    print(f"Sinais coletados: {len(signals)}")
    
    # 2. Processar, Classificar e Salvar
    print("\nPasso 2: Processando, classificando e salvando leads...")
    results = await collector.process_and_save_signals(signals)
    
    print(f"\nResultados do processamento: {len(results)} leads gerados.")
    for res in results:
        print(f" - Lead ID: {res['lead_id']}, Score: {res['score']}")
    
    print("\n=== Fluxo concluído com sucesso! ===")

if __name__ == "__main__":
    asyncio.run(test_full_pipeline())
