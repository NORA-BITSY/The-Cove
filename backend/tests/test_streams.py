from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_streams_empty():
    r = client.get("/api/streams")
    assert r.status_code == 200
    assert r.json() == []
