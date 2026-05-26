 # Arquitetura

  ## Visão Geral
  A API implementa um fluxo de **Policy-Grounded RAG** para análise de conformidade financeira.
  A resposta final do LLM é fundamentada em trechos recuperados da base de conhecimento e retorna fontes auditáveis.

  ## Fluxo

  1. **Ingestão** (`src/rag/ingestion.py`)
  - Leitura de arquivos PDF/TXT em `knowledge_base/`
  - Normalização e chunking
  - Geração de embeddings
  - Upsert no ChromaDB com metadados (`source_document`, `source_chunk_id`, `page_number`)

  2. **Retrieval** (`src/rag/retrieval.py`)
  - Embedding da query
  - Busca vetorial top-k no ChromaDB
  - Re-ranking dos resultados para priorizar relevância semântica

  3. **Análise** (`src/services/compliance_service.py`)
  - Montagem de prompt com strict grounding
  - Chamada ao Azure OpenAI
  - Parse estruturado da resposta JSON
  - Inclusão das fontes usadas na resposta da API

  4. **API** (`src/api/routes.py` e `src/main.py`)
  - Endpoint `POST /analyze`
  - Request/Response com Pydantic
  - Tratamento de erro HTTP

  ## Diagrama de Alto Nível

  flowchart LR
      A[Knowledge Base PDFs/TXTs] --> B[Ingestion Pipeline]
      B --> C[(ChromaDB)]
      D[Query do Usuario] --> E[Retriever]
      C --> E
      E --> F[Re-ranker]
      F --> G[Prompt Grounded]
      G --> H[Azure OpenAI]
      H --> I[Resposta Estruturada + Sources]
