# Guia de Desenvolvimento - Agente Comercial Estético

Este guia explica como testar as funcionalidades implementadas durante esta fase de desenvolvimento.

## Pré-requisitos
- Python 3.10+
- Chave da API OpenAI (opcional para testes de fluxo, obrigatória para classificação real)

## Configuração
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure o arquivo `.env`:
   ```text
   # Provedor: openai, openrouter, ollama
   LLM_PROVIDER=openai
   LLM_MODEL=gpt-4o-mini
   
   OPENAI_API_KEY=sua_chave_aqui
   OPENROUTER_API_KEY=sua_chave_aqui
   
   DATABASE_URL=sqlite:///./sql_app.db
   ```

## Scripts de Teste
Executamos o desenvolvimento em passos validados por scripts:

1. **Inicialização do Banco:**
   ```bash
   python init_db.py
   ```
   Cria as tabelas `leads`, `source_items`, etc.

2. **Teste de Provedores LLM:**
   ```bash
   python test_providers.py
   ```
   Valida a conexão com OpenAI, OpenRouter e Ollama.

3. **Teste de Persistência:**
   ```bash
   python test_db.py
   ```
   Valida se o SQLAlchemy está gravando e lendo corretamente.

3. **Teste de IA (Intent Engine):**
   ```bash
   python test_engine.py
   ```
   Valida a classificação de textos via LLM (requer API Key).

4. **Teste de API:**
   ```bash
   python test_api.py
   ```
   Valida os endpoints FastAPI de gerenciamento de leads.

5. **Teste de Fluxo Completo (E2E):**
   ```bash
   python test_full_pipeline.py
   ```
   Simula a coleta de um sinal, classificação automática e geração de lead no banco.

## Estrutura Atualizada
- `app/db/session.py`: Gerenciamento de conexão com o banco.
- `app/services/collector.py`: Agora orquestra o fluxo de coleta e salvamento.
- `app/services/engine.py`: Integrado com OpenAI para análise semântica.
