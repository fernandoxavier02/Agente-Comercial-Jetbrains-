# Agente de Captação por Intenção — Estética Médica (MVP)

Este projeto implementa a estrutura básica do agente de captação e qualificação de leads para medicina estética, conforme descrito no planejamento do MVP.

## Estrutura do Projeto

```text
app/
├── api/            # Camada de interface (REST API)
│   └── v1/         # Versão 1 da API
├── core/           # Configurações e segurança
├── db/             # Conexão e sessões do banco de dados
├── models/         # Modelos de dados (SQLAlchemy)
├── schemas/        # Esquemas de validação (Pydantic)
├── services/       # Lógica de negócio (Collector, Engine, Composer)
└── main.py         # Ponto de entrada FastAPI
tests/              # Testes automatizados
requirements.txt    # Dependências do projeto
```

## Componentes Implementados

1.  **Signals Collector (`app/services/collector.py`)**: Responsável por buscar sinais de intenção em fontes externas.
2.  **Intent Engine (`app/services/engine.py`)**: Motor de classificação que utiliza IA para identificar dor estética, intenção e fit.
3.  **Lead Scorer (`app/services/engine.py`)**: Algoritmo de priorização de leads baseado em métricas.
4.  **Outreach Composer (`app/services/composer.py`)**: Gerador de abordagens personalizadas com guardrails de compliance.
5.  **API de Leads (`app/api/v1/endpoints/leads.py`)**: Endpoints para gerenciar os leads capturados (Human-in-the-loop).

## Como Operar o Sistema (Guia da Equipe Comercial)

1.  **Inicie o Dashboard:**
    ```bash
    streamlit run app_dashboard_lite.py
    ```
2.  **Captura de Leads:** Clique em "🚀 Start Capture Mission" para buscar interessados em Ultraformer, Morpheus e Bioestimuladores na Grande SP.
3.  **Priorização VIP:** Foque nos leads com "Lead Score" acima de 30. Eles possuem maior poder aquisitivo identificado pela perícia visual.
4.  **Abordagem SDR:** Utilize a estratégia sugerida em "Deep Analysis & SDR Strategy" para iniciar a conversa no WhatsApp com autoridade técnica ou exclusividade.
5.  **Monitoramento de Pipeline:** Acompanhe o valor financeiro total em aberto no topo do painel.

## Funcionalidades de Produção Ativadas:
*   **Investigador de Patrimônio:** Perícia visual para detectar sinais de riqueza.
*   **Geofencing SP Elite:** Foco em bairros como Itaim Bibi e Alphaville.
*   **Agente SDR Integrado:** Sugere perguntas de triagem e tom de voz personalizado.
*   **Calculadora de ROI:** Estima o faturamento potencial (R$) de cada oportunidade.
*   **Busca Real (Opcional):** Suporte para Serper.dev para captura de dados da web em tempo real.

## Compliance (Guardrails)

O sistema foi estruturado para respeitar as regras de compliance médico:
- Sem promessas de resultado.
- Sem diagnósticos automáticos.
- Foco em conteúdo educativo.
- Auditoria de todas as decisões da IA.
