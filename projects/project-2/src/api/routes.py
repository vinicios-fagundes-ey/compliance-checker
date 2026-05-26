from fastapi import APIRouter, HTTPException

from src.api.schemas import AnalysisRequest, AnalysisResponse
from src.services.compliance_service import analyze_text

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse)
def analyze(request: AnalysisRequest) -> AnalysisResponse:
  try:
      return analyze_text(request.text_to_analyze)
  except Exception as e:
      raise HTTPException(status_code=500, detail=repr(e))
