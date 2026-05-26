from pydantic import BaseModel, Field
from typing import List


class AnalysisRequest(BaseModel):
  text_to_analyze: str = Field(..., min_length=10)


class SourceReference(BaseModel):
  source_document: str
  source_chunk_id: str


class AnalysisResponse(BaseModel):
  is_compliant: bool
  reason: str
  mentioned_products: List[str] = []
  sources: List[SourceReference] = []