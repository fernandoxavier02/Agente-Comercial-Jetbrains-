import asyncio
import json
import time
from typing import List, Dict, Any
from app.services.engine import IntentEngine
from app.core.config import settings

# Lista de modelos para testar no OpenRouter
MODELS_TO_TEST = [
    {"provider": "openrouter", "model": "openai/gpt-4o", "alias": "GPT-4o (Standard)"},
    {"provider": "openrouter", "model": "anthropic/claude-3.5-haiku", "alias": "Claude 3.5 Haiku (Precision)"},
    {"provider": "openrouter", "model": "google/gemini-flash-1.5", "alias": "Gemini 1.5 Flash"},
    {"provider": "openrouter", "model": "meta-llama/llama-3.1-70b-instruct", "alias": "Llama 3.1 70B"},
    {"provider": "openrouter", "model": "openai/gpt-4o-mini", "alias": "GPT-4o Mini"}
]

# Casos de teste diversificados
TEST_CASES = [
    {
        "id": "direct_intent",
        "text": "Qual o valor do botox? Tenho rugas na testa que me incomodam muito.",
        "description": "Intenção direta e clara."
    },
    {
        "id": "vague_complaint",
        "text": "Minha pele está estranha ultimamente, cheia de manchas escuras. O que pode ser?",
        "description": "Queixa vaga (melasma?), exige interpretação clínica."
    },
    {
        "id": "high_risk",
        "text": "Quero fazer preenchimento labial mas quero que fique igual ao daquela influencer, bem exagerado e na hora!",
        "description": "Risco de expectativa irreal e urgência inadequada."
    },
    {
        "id": "technical_question",
        "text": "Vocês trabalham com bioestimuladores de colágeno tipo Radiesse ou Sculptra? Sei que são melhores que o ácido hialurônico para flacidez.",
        "description": "Paciente maduro/avançado, termos técnicos."
    }
]

async def benchmark_models():
    print("=== BENCHMARK DE MODELOS LLM (OPENROUTER) ===")
    results = []

    for model_info in MODELS_TO_TEST:
        print(f"\nTesting Model: {model_info['alias']} ({model_info['model']})...")
        engine = IntentEngine(provider=model_info['provider'], model_name=model_info['model'])
        
        model_results = {
            "alias": model_info['alias'],
            "model": model_info['model'],
            "total_time": 0,
            "success_count": 0,
            "avg_lead_score": 0,
            "tests": []
        }

        for case in TEST_CASES:
            start_time = time.time()
            try:
                # Timeout manual simples para não travar o benchmark
                classification = await asyncio.wait_for(engine.classify(case["text"]), timeout=30)
                end_time = time.time()
                
                duration = end_time - start_time
                model_results["total_time"] += duration
                
                # Verificar se não é fallback (labels 'unknown' indicam falha ou fallback no motor)
                is_fallback = classification.get("pain_point", {}).get("label") == "unknown"
                
                if not is_fallback:
                    model_results["success_count"] += 1
                
                model_results["tests"].append({
                    "case": case["id"],
                    "duration": duration,
                    "score": classification["scores"]["lead_score"],
                    "pain_point": classification["pain_point"]["label"],
                    "fallback": is_fallback
                })
                print(f"  [OK] Case {case['id']} - {duration:.2f}s - Score: {classification['scores']['lead_score']}")
            except Exception as e:
                print(f"  [FAIL] Case {case['id']} - Error: {str(e)}")
                model_results["tests"].append({
                    "case": case["id"],
                    "error": str(e)
                })

        if model_results["success_count"] > 0:
            model_results["avg_time"] = model_results["total_time"] / len(TEST_CASES)
            
        results.append(model_results)

    # Relatório Final
    print("\n" + "="*50)
    print("RELATÓRIO DE PERFORMANCE FINAL")
    print("="*50)
    
    # Ordenar por taxa de sucesso e depois por tempo médio
    ranked = sorted(results, key=lambda x: (x['success_count'], -x.get('avg_time', 999)), reverse=True)
    
    for i, res in enumerate(ranked, 1):
        status = "✅ RECOMENDADO" if i == 1 and res['success_count'] == len(TEST_CASES) else ""
        print(f"{i}. {res['alias']}")
        print(f"   Taxa de Sucesso: {res['success_count']}/{len(TEST_CASES)}")
        print(f"   Tempo Médio: {res.get('avg_time', 0):.2f}s")
        print(f"   {status}")
        print("-" * 30)

if __name__ == "__main__":
    if not settings.OPENROUTER_API_KEY:
        print("Erro: OPENROUTER_API_KEY não encontrada no .env")
    else:
        asyncio.run(benchmark_models())
