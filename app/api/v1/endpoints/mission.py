from fastapi import APIRouter, BackgroundTasks
from app.services.collector import SignalsCollector
import asyncio

router = APIRouter()

@router.post("/run")
async def run_mission(background_tasks: BackgroundTasks):
    """
    Dispara a missão de captura em background.
    """
    collector = SignalsCollector()
    queries = [
        "Ultraformer MPT", 
        "Morpheus 8", 
        "Lavieen", 
        "Bioestimuladores de colágeno", 
        "Sculptra Itaim Bibi"
    ]
    
    background_tasks.add_task(collector.fetch_and_process, queries)
    
    return {"message": "Missão de captura iniciada em segundo plano."}

# Adicionar método auxiliar ao SignalsCollector se não existir
async def fetch_and_process_wrapper(queries):
    from app.services.collector import SignalsCollector
    collector = SignalsCollector()
    signals = await collector.fetch_signals(queries)
    await collector.process_and_save_signals(signals)
