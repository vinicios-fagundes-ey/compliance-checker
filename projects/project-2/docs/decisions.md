# Registro de Decisões Arquiteturais (ADRs)

  ## ADR-001: Uso de ChromaDB local
  **Decisão:** usar ChromaDB persistente local em `./data/output/chroma_db`.
  **Motivo:** simplicidade de setup, baixo custo e rapidez para iteração.

  ## ADR-002: Chunking com overlap
  **Decisão:** chunking com `chunk_size` e `chunk_overlap` configuráveis.
  **Motivo:** preservar contexto entre chunks e melhorar recall no retrieval.

  ## ADR-003: IDs determinísticas para idempotência
  **Decisão:** `source_document + page_number + chunk_text` com hash SHA-256 para `chunk_id`.
  **Motivo:** evitar duplicação em reprocessamentos e garantir rastreabilidade.

  ## ADR-004: Re-ranking após retrieval vetorial
  **Decisão:** aplicar re-ranking nos resultados iniciais.
  **Motivo:** melhorar qualidade do topo da lista e relevância para o prompt final.

  ## ADR-005: Resposta com fontes auditáveis
  **Decisão:** incluir `sources` com `source_document` e `source_chunk_id` no schema de resposta.
  **Motivo:** auditabilidade e explicabilidade da análise de conformidade.
