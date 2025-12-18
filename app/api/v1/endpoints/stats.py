from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.session import get_db
from app.models.models import Lead

router = APIRouter()

@router.get("/")
def get_stats(db: Session = Depends(get_db)):
    """
    Retorna estatísticas consolidadas para o dashboard.
    """
    try:
        total_leads = db.query(Lead).count()
        
        # Contar VIP leads (lead_score > 30)
        vip_leads = 0
        total_revenue = 0.0
        
        leads = db.query(Lead).all()
        for lead in leads:
            score = 0
            if lead.scores and isinstance(lead.scores, dict):
                score = lead.scores.get('lead_score', 0)
            
            if score > 30:
                vip_leads += 1
            
            # Calcular revenue estimado baseado no score
            total_revenue += float(score) * 1000  # R$ 1000 por ponto de score
        
        return {
            "total_leads": total_leads,
            "vip_leads": vip_leads,
            "potential_revenue": total_revenue,
            "region_coverage": "Grande São Paulo",
            "last_update": datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Erro no stats endpoint: {e}")
        return {
            "total_leads": 0,
            "vip_leads": 0,
            "potential_revenue": 0,
            "region_coverage": "N/A",
            "last_update": datetime.now().isoformat()
        }
