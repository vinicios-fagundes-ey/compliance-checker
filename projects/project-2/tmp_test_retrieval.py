from src.rag.retrieval import RetrievalService
q = "recomendacao para cliente conservador"
r = RetrievalService().retrieve_with_rerank(q)
print(len(r))
print((r[0].source_document, r[0].source_chunk_id) if r else "sem resultados")
