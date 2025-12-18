import asyncio
import os
from app.services.engine import IntentEngine
from app.core.config import settings

async def test_providers():
    print("--- Testando Provedores de LLM ---")
    
    # 1. Testar OpenRouter (Simulado se sem chave)
    print("\n1. Testando OpenRouter...")
    if not settings.OPENROUTER_API_KEY:
        print("Aviso: OPENROUTER_API_KEY não configurada. O teste falhará ou usará fallback.")
    
    engine_or = IntentEngine(provider="openrouter", model_name="google/gemini-flash-1.5-8b")
    result_or = await engine_or.classify("Tenho interesse em botox")
    print(f"Resultado OpenRouter: {result_or['pain_point']['label']} (Score: {result_or['scores']['lead_score']})")

    # 2. Testar Ollama (Local)
    print("\n2. Testando Ollama...")
    engine_ollama = IntentEngine(provider="ollama", model_name="llama3")
    result_ollama = await engine_ollama.classify("Como tratar melasma?")
    print(f"Resultado Ollama: {result_ollama['pain_point']['label']} (Score: {result_ollama['scores']['lead_score']})")

if __name__ == "__main__":
    asyncio.run(test_providers())
