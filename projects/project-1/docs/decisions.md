 # Registro de Decisões Arquiteturais (ADRs)

  ## ADR-001: FastAPI como framework da API
  - **Decisão:** usar FastAPI para expor o serviço de análise.
  - **Motivo:** rapidez de desenvolvimento, validação nativa com Pydantic e documentação automática via OpenAPI/Swagger.
  - **Impacto:** endpoint `/analyze` com contrato explícito e testável.

  ## ADR-002: Contratos com Pydantic
  - **Decisão:** definir `AnalysisRequest` e `AnalysisResponse` em `src/api/schemas/analysis.py`.
  - **Motivo:** garantir formato previsível de entrada/saída e reduzir erros de integração.
  - **Impacto:** validação automática de payload e respostas padronizadas.

  ## ADR-003: Lógica de negócio separada da camada HTTP
  - **Decisão:** implementar análise em `src/services/compliance_service.py`.
  - **Motivo:** separar responsabilidades (API vs regra de negócio) e facilitar testes.
  - **Impacto:** maior manutenibilidade e facilidade de mock nos testes.

  ## ADR-004: Cliente Azure OpenAI centralizado
  - **Decisão:** encapsular conexão com LLM em `src/core/llm_client.py` (`AzureModel`).
  - **Motivo:** reutilização, configuração central e menor acoplamento.
  - **Impacto:** troca de configuração simplificada via `.env`.

  ## ADR-005: Resposta estruturada do LLM com Instructor
  - **Decisão:** usar `instructor` para retornar `AnalysisResponse` estruturado.
  - **Motivo:** evitar parsing frágil de texto livre.
  - **Impacto:** melhora de confiabilidade no campo `mentioned_products`.