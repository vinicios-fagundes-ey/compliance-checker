from ..core.llm_client import AzureModel
from ..api.schemas.analysis import AnalysisRequest, AnalysisResponse


def analyze_recommendation(request: AnalysisRequest) -> AnalysisResponse:
  llm_client = AzureModel()

  system_prompt = (
      "Você é um analista de compliance de investimentos. "
      "Avalie adequação da recomendação ao perfil do cliente. "
      "Retorne estritamente os campos estruturados solicitados."
  )

  user_prompt = f"""
  Perfil do cliente: {request.client_profile}
  Recomendação: {request.text_to_analyze}

  Regras:
  - is_compliant: true se a recomendação for adequada ao perfil; false caso contrário.
  - reason: justificativa objetiva e curta.
  - mentioned_products: liste produtos de investimento citados no texto (ex.: ações, small caps, CDB, fundos etc.).
  """

  result = llm_client.client.chat.completions.create(
      model=llm_client.deployment,
      response_model=AnalysisResponse,
      temperature=llm_client.temperature,
      max_tokens=llm_client.max_tokens,
      messages=[
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": user_prompt},
      ],
  )

  return result