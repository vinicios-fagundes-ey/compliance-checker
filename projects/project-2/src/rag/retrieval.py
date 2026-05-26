from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List

import chromadb
from sentence_transformers import CrossEncoder, SentenceTransformer

from src.core.settings import settings


@dataclass
class RetrievedChunk:
  source_document: str
  source_chunk_id: str
  page_number: int
  text: str
  retrieval_score: float
  rerank_score: float | None = None


class RetrievalService:
  def __init__(self) -> None:
      self.client = chromadb.PersistentClient(path=settings.vector_db_path)
      self.collection = self.client.get_collection(name=settings.collection_name)
      self.embedder = SentenceTransformer(settings.embedding_model_name)
      self.reranker = None
      try:
          self.reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
      except Exception as e:
          # Ambiente corporativo pode bloquear download do modelo do HF.
          print(f"[WARN] CrossEncoder indisponivel, usando fallback local de rerank. Motivo: {e}")

  def retrieve(self, query: str, top_k: int | None = None) -> List[RetrievedChunk]:
      k = top_k or settings.retrieval_top_k
      q_emb = self.embedder.encode(query, normalize_embeddings=True).tolist()

      result = self.collection.query(
          query_embeddings=[q_emb],
          n_results=k,
          include=["documents", "metadatas", "distances"],
      )

      documents = result.get("documents", [[]])[0]
      metadatas = result.get("metadatas", [[]])[0]
      distances = result.get("distances", [[]])[0]

      chunks: List[RetrievedChunk] = []
      for doc, meta, dist in zip(documents, metadatas, distances):
          chunks.append(
              RetrievedChunk(
                  source_document=meta.get("source_document", "unknown"),
                  source_chunk_id=meta.get("source_chunk_id", "unknown"),
                  page_number=int(meta.get("page_number", 0)),
                  text=doc,
                  retrieval_score=float(dist),
              )
          )
      return chunks

  def rerank(self, query: str, chunks: List[RetrievedChunk], top_k: int | None = None) -> List[RetrievedChunk]:
      if not chunks:
          return []

      if self.reranker is not None:
          pairs = [(query, c.text) for c in chunks]
          scores = self.reranker.predict(pairs)
          for c, score in zip(chunks, scores):
              c.rerank_score = float(score)
      else:
          query_terms = set(re.findall(r"\w+", query.lower()))
          for c in chunks:
              doc_terms = set(re.findall(r"\w+", c.text.lower()))
              overlap = len(query_terms.intersection(doc_terms))
              # score local: overlap lexical + bonus por menor distancia vetorial
              c.rerank_score = float(overlap) + (1.0 / (1.0 + max(c.retrieval_score, 0.0)))

      ordered = sorted(chunks, key=lambda x: x.rerank_score if x.rerank_score is not None else -9999, reverse=True)
      k = top_k or settings.rerank_top_k
      return ordered[:k]

  def retrieve_with_rerank(self, query: str) -> List[RetrievedChunk]:
      initial = self.retrieve(query=query, top_k=settings.retrieval_top_k)
      return self.rerank(query=query, chunks=initial, top_k=settings.rerank_top_k)
