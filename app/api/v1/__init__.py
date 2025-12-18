from fastapi import APIRouter
from app.api.v1.endpoints import leads, mission, stats

api_router = APIRouter()
api_router.include_router(leads.router, prefix="/leads", tags=["leads"])
api_router.include_router(mission.router, prefix="/mission", tags=["mission"])
api_router.include_router(stats.router, prefix="/stats", tags=["stats"])
