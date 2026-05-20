 # Solution Design Document (SDD)

  ## Objetivo
  Construir um serviço especialista de compliance que faça análise inicial de recomendações de investimento.

  ## Escopo do Projeto 1
  - API FastAPI com endpoint `POST /analyze`
  - Contratos Pydantic de request/response
  - Integração com Azure OpenAI
  - Dockerização da aplicação
  - Testes unitários e de integração básicos

  ## Requisitos funcionais
  - Receber `text_to_analyze` e `client_profile`
  - Retornar:
    - `is_compliant` (bool)
    - `reason` (str)
    - `mentioned_products` (list[str])

  ## Requisitos não funcionais
  - Documentação automática via Swagger (`/docs`)
  - Código organizado por camadas (`api`, `services`, `core`)
  - Execução local e containerizada

  ## Estratégia de testes
  - **Unitário:** serviço com mock do cliente LLM
  - **Integração:** endpoints `/health` e `/analyze` com TestClient