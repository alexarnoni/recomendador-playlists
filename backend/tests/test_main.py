from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_recomendar_com_frase_valida():
    response = client.get("/api/recomendar?frase=estou triste hoje")
    assert response.status_code == 200
    data = response.json()
    assert "mensagem" in data
    assert "playlist_1" in data

def test_recomendar_frase_vazia():
    response = client.get("/api/recomendar?frase=")
    assert response.status_code == 400
    assert response.json()["erro"] == "A frase não pode estar vazia."

def test_frase_curta():
    response = client.get("/api/recomendar?frase=ok")
    assert response.status_code == 400
    assert response.json()["erro"] == "A frase é muito curta para análise."
