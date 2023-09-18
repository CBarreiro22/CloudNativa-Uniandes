import json
from datetime import datetime

import pytest
from unittest.mock import patch, MagicMock, Mock
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from src.errors.errors import TokenNotHeaderError, ApiError, InvalidToken
from src.main import app
from src.models.model import db_session, init_db, Model
from src.models.score import Scores
from src.blueprints.scoreOperation import calcular_score, is_valid_token


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_requests():
    with patch('src.blueprints.scoreOperation.requests') as mock_requests:
        yield mock_requests


@pytest.fixture
def mock_sqlalchemy_session():
    with patch('src.models.model.sessionmaker') as mock_sessionmaker:
        mock_session = Mock(spec=Session)
        mock_sessionmaker.return_value = mock_session
        yield mock_session


def test_score_operation(client, mock_requests):
    # Simula una solicitud POST con datos de prueba
    data = {
        "id_offer": "123",
        "id_route": "456"
    }

    # Mockea el token para que sea válido
    token = "valid_token"

    # Configura el comportamiento del mock de las peticiones HTTP
    mock_requests.get.return_value.status_code = 200
    mock_requests.get.return_value.json.return_value = {
        "offer": 100,
        "size": "SMALL",
        "bagCost": 10
    }

    # Realiza la solicitud con el token mockeado
    response = client.post('/score', json=data, headers={"Authorization": f"Bearer {token}"})

    # Asegura que la respuesta sea 200 OK y que contenga "score" en el JSON de la respuesta
    assert response.status_code == 200
    assert "score" in response.json
    assert response.json["score"] == 90


def test_score_operation_with_missing_parameters(client):
    # Prueba la ruta /score sin proporcionar parámetros
    data = {}
    headers = {
        "Authorization": "valid_token"
    }
    response = client.post('/score', json=data, headers=headers)
    assert response.status_code == 400
    assert "error" in response.json
    assert response.json["error"] == "Los parámetros id_offer e id_route son obligatorios"

def test_score_operation_sin_token(client):
    response = client.post(
        '/score',
        json={"id_offer": 1, "id_route": 2},
        headers={"Authorization": ""}
    )

    assert response.status_code == 403


def test_get_score_info(client, mock_requests):
    # Simula una solicitud GET para obtener la información de puntaje
    id_offer = "123"
    token = "valid_token"
    mock_requests.get.return_value.status_code = 200
    mock_score = Scores(id_offer=id_offer, score=50, id_route="123", offer=123, size="SMALL",
                        bagcost=123)  # Crea un puntaje simulado en la base de datos
    db_session.query(Scores).filter_by(id_offer=id_offer).first = mock_score

    response = client.get(f'/score/{id_offer}', headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert "id" in response.json
    assert "Score" in response.json
    assert response.json["Score"] == 90


def test_get_score_info_with_invalid_id(client):
    # Prueba la ruta /score/<id_offer> con un ID no válido
    response = client.get('/score/9999')
    assert response.status_code == 403
    assert "mssg" in response.json
    assert response.json["mssg"] == "El token no está en el encabezado de la solicitud"


def test_calculate_score():
    # Prueba 1: Valores pequeños
    assert calcular_score(100, 'SMALL', 10) == 90

    # Prueba 2: Valores medianos
    assert calcular_score(200, 'MEDIUM', 20) == 190

    # Prueba 3: Valores grandes
    assert calcular_score(300, 'LARGE', 30) == 292.5




def test_health_check(client):
    response = client.get('/score/ping')
    assert response.status_code == 200
    assert response.data == b"pong"


def test_reset_database(client):
    response = client.post('/score/reset')
    assert response.status_code == 200
    assert "msg" in response.json
    assert response.json["msg"] == "Todos los datos fueron eliminados"


def test_model_creation():
    model = Model()
    assert isinstance(model.createdAt, datetime)


def test_model_id():
    model = Model()
    assert model.id is not None


def test_api_error():
    error = ApiError("Custom Error Description")
    assert str(error) == "Custom Error Description"
    assert error.code == 500


def test_token_not_header_error():
    error = TokenNotHeaderError("El token no está en el encabezado de la solicitud")
    assert str(error) == "El token no está en el encabezado de la solicitud"
    assert error.code == 403


def test_invalid_token():
    error = InvalidToken("Token Invalido o esta vencido")
    assert str(error) == "Token Invalido o esta vencido"
    assert error.code == 401
