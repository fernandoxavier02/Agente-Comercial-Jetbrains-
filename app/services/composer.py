from typing import List, Dict, Any

class OutreachComposer:
    """
    Componente F: Abordagem & Mensagem (Outreach Composer)
    Define estratégia (tom, formato, CTA) e gera rascunhos.
    """
    def __init__(self, compliance_rules: List[str] = None):
        self.compliance_rules = compliance_rules or [
            "Proibido promessas de resultado",
            "Proibido diagnóstico",
            "Obrigatório convite para avaliação",
            "Tom educativo"
        ]

    def compose_messages(self, lead_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gera mensagens de abordagem e envia alerta se configurado.
        """
        strategy = "premium_educational"
        messages = [
            f"Olá! Vimos seu interesse em tecnologias de ponta para rejuvenescimento. Na Clínica Médica Mais (Itaim Bibi), somos especialistas em protocolos personalizados com Ultraformer MPT e Bioestimuladores para resultados naturais. Gostaria de conhecer nosso espaço?"
        ]
        triage_questions = [
            "Você já realizou algum procedimento com bioestimuladores ou tecnologias como Ultraformer anteriormente?",
            "Qual sua principal expectativa em relação à naturalidade do resultado?"
        ]

        # Simulação de envio de Alerta (Passo 2)
        # Em produção: requests.post(WEBHOOK_URL, json={"lead": lead_context, "message": messages[0]})
        
        return {
            "strategy": strategy,
            "messages": messages,
            "triage_questions": triage_questions,
            "alert_sent": True
        }
