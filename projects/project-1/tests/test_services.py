from src.api.schemas.analysis import AnalysisRequest, AnalysisResponse
from src.services.compliance_service import analyze_recommendation


class _FakeCompletions:
    def create(self, **kwargs):
        return AnalysisResponse(
            is_compliant=False,
            reason="Inadequado para perfil conservador.",
            mentioned_products=["acoes", "small caps"],
        )


class _FakeChat:
    completions = _FakeCompletions()


class _FakeClient:
    chat = _FakeChat()


class _FakeAzureModel:
    def __init__(self):
        self.client = _FakeClient()
        self.deployment = "fake-deployment"
        self.temperature = 0.3
        self.max_tokens = 1000


def test_analyze_recommendation_returns_structured_response(monkeypatch):
    monkeypatch.setattr("src.services.compliance_service.AzureModel", _FakeAzureModel)

    req = AnalysisRequest(
        text_to_analyze="Recomendo 80% em small caps.",
        client_profile="conservador",
    )

    result = analyze_recommendation(req)

    assert result.is_compliant is False
    assert isinstance(result.reason, str)
    assert "small caps" in result.mentioned_products
