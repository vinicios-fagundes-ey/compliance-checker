from fastapi.testclient import TestClient

from src.api.schemas.analysis import AnalysisResponse
from src.main import app

client = TestClient(app)


def test_healthcheck():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analyze_validation_error():
    response = client.post(
        "/analyze",
        json={"text_to_analyze": "curto", "client_profile": "conservador"},
    )
    assert response.status_code == 422


def test_analyze_success_with_mock(monkeypatch):
    def _fake_analyze_recommendation(_request):
        return AnalysisResponse(
            is_compliant=False,
            reason="Inadequado para perfil conservador.",
            mentioned_products=["acoes", "small caps"],
        )

    monkeypatch.setattr("src.main.analyze_recommendation", _fake_analyze_recommendation)

    response = client.post(
        "/analyze",
        json={
            "text_to_analyze": "Recomendo 80% em small caps para este cliente.",
            "client_profile": "conservador",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["is_compliant"] is False
    assert "small caps" in data["mentioned_products"]
