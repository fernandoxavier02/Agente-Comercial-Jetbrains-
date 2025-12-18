from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime

class SourceItemBase(BaseModel):
    source: str
    url: str
    author_handle: str
    timestamp: datetime
    text: str
    raw_metadata: Optional[Dict[str, Any]] = None

class LeadBase(BaseModel):
    source_item_id: int
    clinic_id: int
    scores: Dict[str, Any]
    labels: Dict[str, Any]
    evidence_snippets: Optional[List[Any]] = None  # Aceita strings ou dicts
    status: str = "pending"

class OutreachDraftBase(BaseModel):
    lead_id: int
    strategy: str
    messages: List[str]
    triage_questions: List[str]

class LeadUpdate(BaseModel):
    status: str

class LeadResponse(LeadBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
