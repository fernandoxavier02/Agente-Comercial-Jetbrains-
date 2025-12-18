import streamlit as st
import pandas as pd
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.models import Lead, SourceItem
from app.services.composer import OutreachComposer
import json

# Page Config
st.set_page_config(
    page_title="Elite Leads Hub - Clínica Médica Mais",
    page_icon="💎",
    layout="wide"
)

# Custom Style
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; }
    .lead-card { border: 1px solid #333; padding: 20px; border-radius: 10px; margin-bottom: 20px; background-color: #161b22; }
    .vip-badge { background-color: #ffd700; color: black; padding: 2px 8px; border-radius: 5px; font-weight: bold; }
    .tag-lite { background-color: #0068c9; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.8em; margin-right: 5px; display: inline-block; }
    </style>
    """, unsafe_allow_html=True)

st.title("💎 Elite Leads Hub (Lite)")
st.subheader("Intelligence & Capture Panel - Clínica Médica Mais")

def get_leads():
    db = SessionLocal()
    try:
        leads = db.query(Lead).order_by(Lead.scores['lead_score'].desc()).all()
        return leads
    finally:
        db.close()

def get_source_item(item_id):
    db = SessionLocal()
    try:
        return db.query(SourceItem).filter(SourceItem.id == item_id).first()
    finally:
        db.close()

# Sidebar
st.sidebar.header("⚙️ Mission Control")

if st.sidebar.button("🚀 Start Capture Mission"):
    with st.spinner("Searching for elite leads in SP..."):
        import asyncio
        from mission_capture_elite import run_capture_mission
        asyncio.run(run_capture_mission())
    st.sidebar.success("Mission completed!")
    st.rerun()

leads = get_leads()

if not leads:
    st.warning("No leads captured yet. Click 'Start Capture Mission'.")
else:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Leads", len(leads))
    col2.metric("VIPs", len([l for l in leads if l.scores.get('lead_score', 0) > 30]))
    
    # Calcular Pipeline Total (Passo 4)
    from app.services.roi_engine import ROIEngine
    roi = ROIEngine()
    total_pipeline = sum([roi.estimate_revenue({"labels": l.labels})['estimated_value'] for l in leads])
    col3.metric("Pipeline Potencial", f"R$ {total_pipeline:,.2f}")

    st.divider()

    for lead in leads:
        source_item = get_source_item(lead.source_item_id)
        score = lead.scores.get('lead_score', 0)
        is_vip = score > 30
        
        # Estimar Revenue por Lead
        rev_data = roi.estimate_revenue({"labels": lead.labels})
        
        with st.container():
            cols = st.columns([1, 4, 2])
            
            with cols[0]:
                img_url = source_item.raw_metadata.get('author_image') if source_item and source_item.raw_metadata else None
                if img_url: st.image(img_url, width=120)
                else: st.markdown("👤 No Image")
            
            with cols[1]:
                status_label = "💎 VIP ELITE" if is_vip else "✅ QUALIFIED"
                st.markdown(f"### {source_item.author_handle if source_item else 'Anonymous'} | <span class='vip-badge'>{status_label}</span>", unsafe_allow_html=True)
                st.write(f"💬 *\"{source_item.text if source_item else ''}\"*")
                
                # Tags (Lite version without annotated_text)
                tags = lead.labels.get('visual_profile', [])
                for tag in tags:
                    st.markdown(f"<span class='tag-lite'>{tag}</span>", unsafe_allow_html=True)
                
                with st.expander("🔍 Deep Analysis & SDR Strategy"):
                    st.write(f"**Visual Justification:** {lead.scores.get('visual_justification', 'N/A')}")
                    st.write(f"**Subliminal Signals:** {', '.join(lead.scores.get('subliminal_signals', [])) if isinstance(lead.scores.get('subliminal_signals'), list) else 'N/A'}")
                    
                    # SDR Strategy (Passo 3)
                    from app.services.sdr_agent import SDRAgent
                    sdr = SDRAgent()
                    flow = sdr.generate_triage_flow({"labels": lead.labels, "scores": lead.scores})
                    st.info(f"🎯 **SDR Opening:** {flow['opening_statement']}")
                    st.write("**Recommended Triage:**")
                    for q in flow['triage_questions']:
                        st.write(f"- {q}")

            with cols[2]:
                st.metric("Lead Score", f"{score:.1f}")
                st.write(f"💰 **Est. Revenue:** R$ {rev_data['estimated_value']:,.2f}")
                st.caption(f"Ref: {rev_data['service']}")
                
                if st.button("📱 WhatsApp Approach", key=f"btn_{lead.id}"):
                    composer = OutreachComposer()
                    context = {"pain_point": lead.labels.get('pain_point'), "intent_stage": lead.labels.get('intent_stage'), "author_handle": source_item.author_handle if source_item else "Client"}
                    outreach = composer.compose_messages(context)
                    st.code(outreach['messages'][0], language="text")

            st.divider()
