from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class SourceItem(Base):
    __tablename__ = "source_items"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String)
    url = Column(String)
    author_handle = Column(String)
    timestamp = Column(DateTime)
    text = Column(Text)
    raw_metadata = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    source_item_id = Column(Integer, ForeignKey("source_items.id"))
    clinic_id = Column(Integer)
    scores = Column(JSON)  # {fit, intent, urgency, maturity, risk, visual_fit, lead_score}
    labels = Column(JSON)  # {pain_point, intent_stage, maturity, visual_profile}
    evidence_snippets = Column(JSON)
    status = Column(String, default="pending")  # pending, approved, rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class OutreachDraft(Base):
    __tablename__ = "outreach_drafts"
    id = Column(Integer, primary_key=True, index=True)
    lead_id = Column(Integer, ForeignKey("leads.id"))
    strategy = Column(String)
    messages = Column(JSON)
    triage_questions = Column(JSON)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    event = Column(String)
    actor = Column(String)
    model_version = Column(String)
    prompt_version = Column(String)
    payload = Column(JSON)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
