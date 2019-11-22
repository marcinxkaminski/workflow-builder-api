from starlette.testclient import TestClient
from main import app


client = TestClient(app)


def test_get_availble_workflow_elements():
    response = client.get("/api/workflow-builder/elements")
    assert response.status_code == 200
    assert response.json() is not None
