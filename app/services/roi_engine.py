from typing import Dict, Any

class ROIEngine:
    """
    Componente I: Calculadora de ROI e Faturamento Estimado.
    Baseado na tabela de preços Tier 1 da Clínica Médica Mais.
    """
    def __init__(self):
        # Valores médios de ticket (R$) por tecnologia/serviço
        self.prices = {
            "Ultraformer MPT": 6000.0,
            "Morpheus 8": 8000.0,
            "Lavieen": 2500.0,
            "Botox": 1800.0,
            "Preenchimento": 3500.0,
            "Bioestimuladores": 5000.0,
            "Sculptra": 5500.0,
            "Radiesse": 4500.0,
            "Protocolo Full Face": 25000.0
        }

    def estimate_revenue(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calcula o faturamento potencial baseado no interesse e tier do lead.
        """
        pain_point = lead_data.get('labels', {}).get('pain_point', '').lower()
        tier = lead_data.get('labels', {}).get('tier', 'Standard')
        
        # Identificar qual serviço o lead busca
        base_value = 2500.0 # Valor padrão mínimo
        service_found = "Consulta / Geral"
        
        for service, price in self.prices.items():
            if service.lower() in pain_point:
                base_value = price
                service_found = service
                break
        
        # Multiplicador de Tier (VIPs tendem a fazer protocolos combinados)
        multiplier = 1.0
        if tier == "VIP":
            multiplier = 2.5 # VIPs costumam fechar protocolos de 25k+
            service_found = f"Protocolo VIP ({service_found}+)"
        elif tier == "Platinum":
            multiplier = 1.8
            service_found = f"Protocolo Premium ({service_found}+)"
            
        estimated_value = base_value * multiplier
        
        return {
            "service": service_found,
            "estimated_value": estimated_value,
            "currency": "R$"
        }
