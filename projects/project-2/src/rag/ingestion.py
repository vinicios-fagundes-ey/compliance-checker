from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import chromadb
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

from src.core.settings import settings


@dataclass
class ChunkRecord:
  chunk_id: str
  text: str
  source_document: str
  page_number: int
  chunk_index: int


def normalize_text(text: str) -> str:
  text = text.replace("\x00", " ")
  text = re.sub(r"\s+", " ", text).strip()
  return text


def chunk_text(text: str, chunk_size: int, chunk_overlap: int) -> Iterable[str]:
  if not text:
      return []

  if chunk_overlap >= chunk_size:
      raise ValueError("chunk_overlap must be smaller than chunk_size")

  chunks = []
  start = 0
  step = chunk_size - chunk_overlap

  while start < len(text):
      end = start + chunk_size
      part = text[start:end].strip()
      if part:
          chunks.append(part)
      start += step

  return chunks


def build_chunk_id(source_document: str, page_number: int, chunk_content: str) -> str:
  payload = f"{source_document}|{page_number}|{chunk_content}".encode("utf-8")
  return hashlib.sha256(payload).hexdigest()


def extract_pdf_chunks(file_path: Path, chunk_size: int, chunk_overlap: int) -> list[ChunkRecord]:
  reader = PdfReader(str(file_path))
  records: list[ChunkRecord] = []

  for i, page in enumerate(reader.pages, start=1):
      raw = page.extract_text() or ""
      text = normalize_text(raw)
      if not text:
          continue

      parts = chunk_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
      for j, part in enumerate(parts, start=1):
          cid = build_chunk_id(file_path.name, i, part)
          records.append(
              ChunkRecord(
                  chunk_id=cid,
                  text=part,
                  source_document=file_path.name,
                  page_number=i,
                  chunk_index=j,
              )
          )
  return records


def extract_txt_chunks(file_path: Path, chunk_size: int, chunk_overlap: int) -> list[ChunkRecord]:
  raw = file_path.read_text(encoding="utf-8", errors="ignore")
  text = normalize_text(raw)
  if not text:
      return []

  records: list[ChunkRecord] = []
  parts = chunk_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

  for j, part in enumerate(parts, start=1):
      cid = build_chunk_id(file_path.name, 1, part)
      records.append(
          ChunkRecord(
              chunk_id=cid,
              text=part,
              source_document=file_path.name,
              page_number=1,
              chunk_index=j,
          )
      )
  return records


def collect_chunks(knowledge_base_dir: Path) -> list[ChunkRecord]:
  all_records: list[ChunkRecord] = []

  for file_path in sorted(knowledge_base_dir.iterdir()):
      if file_path.is_dir():
          continue

      suffix = file_path.suffix.lower()
      if suffix == ".pdf":
          all_records.extend(
              extract_pdf_chunks(
                  file_path,
                  chunk_size=settings.chunk_size,
                  chunk_overlap=settings.chunk_overlap,
              )
          )
      elif suffix == ".txt":
          all_records.extend(
              extract_txt_chunks(
                  file_path,
                  chunk_size=settings.chunk_size,
                  chunk_overlap=settings.chunk_overlap,
              )
          )

  return all_records


def upsert_chunks(records: list[ChunkRecord]) -> None:
  Path(settings.vector_db_path).mkdir(parents=True, exist_ok=True)

  client = chromadb.PersistentClient(path=settings.vector_db_path)
  collection = client.get_or_create_collection(name=settings.collection_name)

  model = SentenceTransformer(settings.embedding_model_name)

  batch_size = 64
  total = len(records)

  for i in range(0, total, batch_size):
      batch = records[i : i + batch_size]

      ids = [r.chunk_id for r in batch]
      docs = [r.text for r in batch]
      metas = [
          {
              "source_document": r.source_document,
              "source_chunk_id": r.chunk_id,
              "page_number": r.page_number,
              "chunk_index": r.chunk_index,
          }
          for r in batch
      ]

      embeddings = model.encode(docs, normalize_embeddings=True).tolist()

      # upsert garante idempotencia (mesmo ID nao duplica)
      collection.upsert(
          ids=ids,
          documents=docs,
          metadatas=metas,
          embeddings=embeddings,
      )

      print(f"Processed {min(i + batch_size, total)}/{total} chunks")


def run_ingestion() -> None:
  project_root = Path(__file__).resolve().parents[2]
  knowledge_base_dir = project_root / "knowledge_base"

  if not knowledge_base_dir.exists():
      raise FileNotFoundError(f"knowledge_base not found: {knowledge_base_dir}")

  records = collect_chunks(knowledge_base_dir)
  print(f"Total chunks collected: {len(records)}")

  if not records:
      print("No chunks found to ingest.")
      return

  upsert_chunks(records)
  print("Ingestion completed successfully.")


if __name__ == "__main__":
  run_ingestion()