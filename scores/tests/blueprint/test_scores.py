import pytest
from unittest.mock import Mock, patch
from src.main import app
from src.models.model import db_session
from src.models.score import Scores


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_requests():
    with patch('src.blueprints.scoreOperation.requests') as mock_requests:
        yield mock_requests


def test_score_operation(client, mock_requests):
    # Simula una solicitud POST con datos de prueba
    data = {
        "id_offer": "123",
        "id_route": "456"
    }
    token = "mocked_token"
    mock_requests.headers.get.return_value = token
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "offer": 100,
        "size": "SMALL",
        "bagCost": 10
    }
    mock_requests.get.side_effect = [mock_response, mock_response]

    response = client.post('/score', json=data, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert "score" in response.json


def test_get_score_info(client, mock_requests):
    # Simula una solicitud GET para obtener la información de puntaje
    id_offer = "123"
    token = "mocked_token"
    mock_requests.headers.get.return_value = token
    mock_score = Scores(id_offer=id_offer, score=50, id_route="123", offer=123,size="SMALL",bagcost=123)  # Crea un puntaje simulado en la base de datos
    db_session.query(Scores).filter_by(id_offer=id_offer).first = mock_score

    response = client.get(f'/score/{id_offer}', headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert "id" in response.json
    assert "Score" in response.json


def test_health_check(client):
    response = client.get('/score/ping')
    assert response.status_code == 200
    assert response.data == b"pong"


def test_reset_database(client):
    response = client.post('/score/reset')
    assert response.status_code == 200
    assert "msg" in response.json
