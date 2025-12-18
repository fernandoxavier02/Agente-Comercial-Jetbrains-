import logging
from typing import Dict, Any, List
from app.services.engine import IntentEngine

class SDRAgent:
    """
    Componente H: Agente SDR (Sales Development Representative)
    Responsável pela triagem técnica e preparação para o agendamento na Clínica Médica Mais.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.engine = IntentEngine()
        
    def generate_triage_flow(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera um fluxo de conversação personalizado com base na dor e maturidade do lead.
        """
        pain_point = lead_data.get('labels', {}).get('pain_point', 'estética')
        maturity = lead_data.get('labels', {}).get('maturity', 'iniciante')
        tier = lead_data.get('labels', {}).get('tier', 'Standard')
        
        # Estratégia de SDR baseada em Tier e Maturidade
        if tier == "VIP" or tier == "Platinum":
            strategy = "Consultiva de Alto Padrão (Exclusividade)"
            opening = f"Como você já conhece os benefícios de tecnologias como {pain_point}, nossa consultoria foca em protocolos exclusivos e discrição absoluta."
        else:
            strategy = "Educativa Técnica (Autoridade)"
            opening = f"Entendo perfeitamente sua busca por {pain_point}. Na Clínica Mais, priorizamos a ciência por trás de cada resultado natural."

        questions = [
            f"Em relação ao tratamento de {pain_point}, qual resultado você mais valoriza: durabilidade ou naturalidade imediata?",
            "Você tem preferência por alguma das nossas tecnologias específicas, como Ultraformer MPT ou Morpheus 8?",
            "Para sua comodidade, você prefere horários no período da manhã ou tarde no Itaim Bibi?"
        ]

        return {
            "strategy": strategy,
            "opening_statement": opening,
            "triage_questions": questions,
            "appointment_intent": "high" if tier in ["VIP", "Platinum"] else "medium"
        }

    def prepare_booking_summary(self, lead_data: Dict[str, Any]) -> str:
        """
        Prepara um resumo executivo para o consultor humano realizar o fechamento.
        """
        return f"""
        RESUMO SDR - CLÍNICA MAIS
        -------------------------
        Lead: {lead_data.get('author_handle')}
        Perfil: {lead_data.get('labels', {}).get('tier')} ({lead_data.get('scores', {}).get('lead_score')} pts)
        Interesse: {lead_data.get('labels', {}).get('pain_point')}
        Maturidade: {lead_data.get('labels', {}).get('maturity')}
        
        AÇÃO RECOMENDADA: {lead_data.get('outreach_strategy', 'Abordagem Padrão')}
        FOCO: {lead_data.get('subliminal_signals', ['Qualidade técnica'])[0]}
        """
