from __future__ import annotations

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.rag.retrieval import RetrievalService

QUERIES = [
    "cliente conservador recebendo recomendacao de fundo agressivo",
    "como verificar suitability na distribuicao de produtos de investimento",
    "recomendacao de renda variavel para perfil moderado",
]


def show_results(title: str, chunks):
    print(f"\n=== {title} ===")
    for i, c in enumerate(chunks, start=1):
        print(
            f"{i}. doc={c.source_document} | chunk={c.source_chunk_id[:12]}... | "
            f"retrieval={c.retrieval_score:.4f} | rerank={c.rerank_score}"
        )


def main():
    service = RetrievalService()

    for q in QUERIES:
        print("\n" + "=" * 120)
        print(f"QUERY: {q}")

        before = service.retrieve(q, top_k=8)
        show_results("ANTES DO RE-RANK", before)

        after = service.rerank(q, before, top_k=4)
        show_results("DEPOIS DO RE-RANK", after)

        print("\nResumo:")
        print("- Compare se os chunks do topo apos re-rank estao semanticamente mais alinhados a query.")
        print("- Verifique se documentos de politica/suitability ficaram acima de trechos genericos.")


if __name__ == "__main__":
    main()