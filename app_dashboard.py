import streamlit as st
import pandas as pd
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.models import Lead, SourceItem
from app.services.composer import OutreachComposer
from st_annotated_text import annotated_text
import json

# Configuração da Página
st.set_page_config(
    page_title="Elite Leads Hub - Clínica Médica Mais",
    page_icon="💎",
    layout="wide"
)

# Estilo Customizado (Dark/Premium)
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
    }
    .lead-card {
        border: 1px solid #333;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        background-color: #161b22;
    }
    .vip-badge {
        background-color: #ffd700;
        color: black;
        padding: 2px 8px;
        border-radius: 5px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Título
st.title("💎 Elite Leads Hub")
st.subheader("Painel de Inteligência e Captação - Clínica Médica Mais")

# Funções de Dados
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
st.sidebar.image("https://clinicamais.club/wp-content/uploads/2021/04/logo-clinica-mais.png", width=200)
st.sidebar.divider()
st.sidebar.header("⚙️ Controle de Missão")

if st.sidebar.button("🚀 Iniciar Nova Captura"):
    with st.spinner("Buscando leads de elite em SP..."):
        import asyncio
        from mission_capture_elite import run_capture_mission
        asyncio.run(run_capture_mission())
    st.sidebar.success("Missão concluída!")
    st.rerun()

st.sidebar.divider()
st.sidebar.info("Este dashboard prioriza leads de Alto Ticket (Tier 1) na região da Grande São Paulo.")

# Carregar Leads
leads = get_leads()

if not leads:
    st.warning("Nenhum lead capturado ainda. Clique em 'Iniciar Nova Captura' na barra lateral.")
else:
    # Métricas Rápidas
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Leads", len(leads))
    col2.metric("VIPs (Score > 30)", len([l for l in leads if l.scores.get('lead_score', 0) > 30]))
    col3.metric("Região SP", "100%", delta="Grande SP")

    st.divider()

    # Listagem de Leads
    for lead in leads:
        source_item = get_source_item(lead.source_item_id)
        score = lead.scores.get('lead_score', 0)
        is_vip = score > 30
        
        with st.container():
            # Card do Lead
            cols = st.columns([1, 4, 2])
            
            with cols[0]:
                # Imagem ou Placeholder
                img_url = source_item.raw_metadata.get('author_image') if source_item and source_item.raw_metadata else None
                if img_url:
                    st.image(img_url, width=120)
                else:
                    st.markdown("👤 No Image")
            
            with cols[1]:
                # Cabeçalho do Lead
                status_label = "💎 VIP ELITE" if is_vip else "✅ QUALIFICADO"
                st.markdown(f"### {source_item.author_handle if source_item else 'Anônimo'} | <span class='vip-badge'>{status_label}</span>", unsafe_allow_html=True)
                
                # Texto do Lead
                st.write(f"💬 *\"{source_item.text if source_item else ''}\"*")
                
                # Tags e Sinais
                tags = lead.labels.get('visual_profile', [])
                if tags:
                    annotated_text(*[(tag, "", "#0068c9") for tag in tags])
                
                # Justificativa IA
                with st.expander("🔍 Ver Perícia Detalhada"):
                    st.write(f"**Justificativa Visual:** {lead.scores.get('visual_justification', 'N/A')}")
                    st.write(f"**Sinais Subliminares:** {', '.join(lead.scores.get('subliminal_signals', [])) if isinstance(lead.scores.get('subliminal_signals'), list) else 'N/A'}")
                    st.write(f"**Localização Detectada:** {lead.scores.get('detected_location', 'Grande São Paulo')}")

            with cols[2]:
                # Score e Ações
                st.metric("Lead Score", f"{score:.1f}")
                
                # Gerar Abordagem
                composer = OutreachComposer()
                # Simular contexto para o composer
                context = {
                    "pain_point": lead.labels.get('pain_point'),
                    "intent_stage": lead.labels.get('intent_stage'),
                    "author_handle": source_item.author_handle if source_item else "Cliente"
                }
                outreach = composer.compose_messages(context)
                
                if st.button("📱 Gerar Abordagem WhatsApp", key=f"btn_{lead.id}"):
                    st.code(outreach['messages'][0], language="text")
                    st.caption("Perguntas de triagem sugeridas:")
                    for q in outreach['triage_questions']:
                        st.write(f"- {q}")

            st.divider()
