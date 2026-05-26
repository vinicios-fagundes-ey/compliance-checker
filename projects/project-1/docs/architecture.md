 # Arquitetura

  ## Visão geral
  A solução é uma API REST em FastAPI que recebe uma recomendação de investimento e um perfil de cliente, consulta um LLM (Azure OpenAI) e
  retorna análise estruturada de conformidade.

  ## Componentes
  - **API (`src/main.py`)**
    - Endpoints: `GET /health`, `POST /analyze`
  - **Schemas (`src/api/schemas/analysis.py`)**
    - `AnalysisRequest`, `AnalysisResponse`
  - **Serviço (`src/services/compliance_service.py`)**
    - Monta prompt e chama o cliente LLM
  - **Core (`src/core/llm_client.py`)**
    - Inicialização e invocação do Azure OpenAI
  - **Configuração**
    - Variáveis via `.env`

  ## Fluxo
  1. Cliente chama `POST /analyze`
  2. FastAPI valida request com Pydantic
  3. Serviço chama Azure OpenAI via `AzureModel`
  4. LLM retorna resposta estruturada (`AnalysisResponse`)
  5. API devolve JSON padronizado