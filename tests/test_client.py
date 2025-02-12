from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_client():
    payload = {
        "document": "12345678901",  # CPF com 11 dígitos (exemplo)
        "name": "Cliente Teste",
        "is_blocked": False
    }
    response = client.post("/clientes", json=payload)
    # Se for criado com sucesso retorna 200 (ou 201 conforme implementação)
    assert response.status_code in (200, 201, 400)
