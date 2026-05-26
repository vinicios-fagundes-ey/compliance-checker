from __future__ import annotations

import json

from openai import AzureOpenAI

from src.api.schemas import AnalysisResponse, SourceReference
from src.core.settings import settings
from src.rag.retrieval import RetrievalService


def _build_prompt(user_text: str, contexts: list[str]) -> str:
  context_block = "\n\n---\n\n".join(contexts)
  return f"""
Voce e um analista de compliance financeiro.
Use SOMENTE o contexto abaixo para decidir.
Se nao houver base suficiente no contexto, diga explicitamente.

CONTEXTO:
{context_block}

TEXTO PARA ANALISAR:
{user_text}

Responda em JSON com os campos:
- is_compliant (boolean)
- reason (string)
- mentioned_products (array de strings)
""".strip()


def analyze_text(text_to_analyze: str) -> AnalysisResponse:
  retrieval = RetrievalService()
  chunks = retrieval.retrieve_with_rerank(text_to_analyze)

  contexts = [c.text for c in chunks]
  sources = [
      SourceReference(
          source_document=c.source_document,
          source_chunk_id=c.source_chunk_id,
      )
      for c in chunks
  ]

  prompt = _build_prompt(text_to_analyze, contexts)

  client = AzureOpenAI(
      api_key=settings.azure_openai_key,
      api_version=settings.azure_openai_api_version,
      azure_endpoint=settings.azure_openai_endpoint,
  )

  resp = client.chat.completions.create(
      model=settings.azure_deployment_name,
      messages=[
          {"role": "system", "content": "Responda apenas JSON valido."},
          {"role": "user", "content": prompt},
      ],
      temperature=0,
      response_format={"type": "json_object"},
  )

  raw = (resp.choices[0].message.content or "").strip()

  try:
      data = json.loads(raw)
  except Exception as e:
      raise ValueError(f"LLM retornou JSON invalido: {raw[:500]} | erro: {e}") from e

  return AnalysisResponse(
      is_compliant=bool(data.get("is_compliant", False)),
      reason=str(data.get("reason", "")),
      mentioned_products=list(data.get("mentioned_products", [])),
      sources=sources,
  )
