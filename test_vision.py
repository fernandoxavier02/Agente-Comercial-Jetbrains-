import asyncio
import json
from app.services.engine import VisionEngine
from app.core.config import settings

async def test_vision():
    print("--- Testando Camada de Visão Computacional ---")
    print(f"Model: {settings.VISION_MODEL}")
    
    vision = VisionEngine()
    
    # URL de uma imagem de exemplo (Mulher bem cuidada em ambiente premium - Unsplash)
    image_url = "https://images.unsplash.com/photo-1594744803329-e58b31de8bf5?auto=format&fit=crop&q=80&w=600"
    
    print(f"\nAnalisando imagem: {image_url}")
    result = await vision.analyze_profile_image(image_url)
    
    print("\nResultado da Análise Visual:")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    if not settings.OPENROUTER_API_KEY:
        print("Erro: OPENROUTER_API_KEY não encontrada.")
    else:
        asyncio.run(test_vision())
