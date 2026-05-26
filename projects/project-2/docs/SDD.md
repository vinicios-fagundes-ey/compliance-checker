 # Solution Design Document (SDD)

  ## Objetivo
  Evoluir a API de compliance para um sistema RAG confiável, com grounding em documentos regulatórios e políticas internas.

  ## Componentes
  - `src/rag/ingestion.py`: pipeline de ingestão e indexação vetorial
  - `src/rag/retrieval.py`: retrieval semântico + re-ranking
  - `src/services/compliance_service.py`: orquestração RAG + chamada LLM
  - `src/api/schemas/analysis.py`: contratos de entrada/saída
  - `src/api/routes.py`: endpoint `/analyze`

  ## Contratos

  ### Input
  - `text_to_analyze: str`

  ### Output
  - `is_compliant: bool`
  - `reason: str`
  - `mentioned_products: list[str]`
  - `sources: list[{source_document, source_chunk_id}]`

  ## Requisitos Não Funcionais
  - Idempotência na ingestão
  - Observabilidade de erros na API
  - Auditabilidade por fonte/chunk
  - Configuração por variáveis de ambiente (`src/core/settings.py`)

  ## Validação
  - Ingestão executada duas vezes sem duplicar dados
  - Retrieval com e sem re-ranking comparado em 3 queries
  - Endpoint `/analyze` retornando resposta estruturada com fontes