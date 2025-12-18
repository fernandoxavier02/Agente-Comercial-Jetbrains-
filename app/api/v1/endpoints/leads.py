from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas.schemas import LeadResponse, LeadUpdate
from app.models.models import Lead
from app.db.session import get_db

router = APIRouter()

@router.get("/")
def read_leads(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    leads = db.query(Lead).offset(skip).limit(limit).all()
    # Retorna JSON diretamente sem validação Pydantic
    result = []
    for lead in leads:
        result.append({
            "id": lead.id,
            "source_item_id": lead.source_item_id,
            "clinic_id": lead.clinic_id,
            "scores": lead.scores or {},
            "labels": lead.labels or {},
            "status": lead.status,
            "created_at": lead.created_at.isoformat() if lead.created_at else None
        })
    return JSONResponse(content=result)

@router.get("/{lead_id}", response_model=LeadResponse)
def read_lead(lead_id: int, db: Session = Depends(get_db)):
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    return db_lead

@router.put("/{lead_id}", response_model=LeadResponse)
def update_lead(lead_id: int, lead_in: LeadUpdate, db: Session = Depends(get_db)):
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if db_lead is None:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    db_lead.status = lead_in.status
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead
