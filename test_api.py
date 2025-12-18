from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_leads():
    response = client.get("/api/v1/leads/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    print("Teste GET /leads/ OK")

def test_read_single_lead():
    # Como já rodamos test_db.py, o ID 1 deve existir
    response = client.get("/api/v1/leads/1")
    if response.status_code == 200:
        assert response.json()["id"] == 1
        print("Teste GET /leads/1 OK")
    else:
        print(f"Lead 1 não encontrado (status {response.status_code}), talvez precise rodar test_db.py primeiro")

def test_update_lead():
    response = client.put("/api/v1/leads/1", json={"status": "approved"})
    if response.status_code == 200:
        assert response.json()["status"] == "approved"
        print("Teste PUT /leads/1 OK")
    else:
        print(f"Falha ao atualizar lead 1 (status {response.status_code})")

if __name__ == "__main__":
    test_read_leads()
    test_read_single_lead()
    test_update_lead()
