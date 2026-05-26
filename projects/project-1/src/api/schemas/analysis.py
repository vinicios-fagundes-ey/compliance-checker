from pydantic import BaseModel, Field
from typing import List


class AnalysisRequest(BaseModel):
  text_to_analyze: str = Field(
      ...,
      min_length=10,
      description="Texto da recomendação a ser analisada."
  )
  client_profile: str = Field(
      ...,
      description="Perfil de risco do cliente (ex: conservador, moderado, agressivo)."
  )


class AnalysisResponse(BaseModel):
  is_compliant: bool = Field(
      ...,
      description="Indica se a recomendação está em conformidade."
  )
  reason: str = Field(
      ...,
      description="Justificativa da análise."
  )
  mentioned_products: List[str] = Field(
      default_factory=list,
      description="Produtos de investimento mencionados no texto."
  )
