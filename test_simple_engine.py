import asyncio
from app.services.engine import IntentEngine
from app.core.config import settings

async def test_simple_classification():
    print("--- Testando Classificação com OpenRouter ---")
    print(f"Provider: {settings.LLM_PROVIDER}")
    print(f"Model: {settings.LLM_MODEL}")
    print(f"Key (primeiros caracteres): {settings.OPENROUTER_API_KEY[:10]}...")
    
    engine = IntentEngine()
    text = "Olá, gostaria de saber o valor da aplicação de botox para rugas na testa. Tenho 35 anos."
    
    print(f"\nClassificando texto: '{text}'")
    result = await engine.classify(text)
    
    import json
    print("\nResultado Completo:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(test_simple_classification())
