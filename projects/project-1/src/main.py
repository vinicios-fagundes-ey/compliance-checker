from fastapi import FastAPI, HTTPException
from .api.schemas.analysis import AnalysisRequest, AnalysisResponse
from .services.compliance_service import analyze_recommendation

app = FastAPI(
  title="Compliance Checker API",
  version="1.0.0",
  description="API para análise de conformidade de recomendações de investimento."
)


@app.get("/health")
def health_check():
  return {"status": "ok"}


@app.post("/analyze", response_model=AnalysisResponse)
def analyze(request: AnalysisRequest):
  try:
      return analyze_recommendation(request)
  except ValueError as e:
      # Ex.: erro de configuração do Azure no .env
      raise HTTPException(status_code=503, detail=str(e))
  except Exception:
      raise HTTPException(status_code=500, detail="Erro interno ao analisar recomendação.")