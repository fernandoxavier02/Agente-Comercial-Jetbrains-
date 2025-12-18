import asyncio
import json
from app.services.engine import IntentEngine
from app.core.config import settings

async def test_subliminal():
    print("--- Testando Camada de Sinais Subliminares ---")
    
    engine = IntentEngine()
    
    # Exemplo de texto com sinais de alto padrão (uso de tecnologia cara e refinamento)
    text = "Estou buscando um protocolo de bioestimuladores, talvez Sculptra, para manter o efeito natural que já tenho. Prefiro algo discreto e exclusivo, sem pressa, focado na manutenção do colágeno."
    
    print(f"\nAnalisando texto: '{text}'")
    result = await engine.classify(text)
    
    print("\nResultado da Inteligência Social:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    if not settings.OPENROUTER_API_KEY:
        print("Erro: OPENROUTER_API_KEY não encontrada.")
    else:
        asyncio.run(test_subliminal())
