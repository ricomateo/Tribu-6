from fastapi.testclient import TestClient

from main import app

ENDPOINT = "/projects"


def test_create_hero(client: TestClient):
    response = client.get(ENDPOINT + "/get_projects")
    app.dependency_overrides.clear()

    assert response.status_code == 200


# from fastapi.testclient import TestClient

# from main import app


# client = TestClient(app)


# def test_read_item():
#     response = client.get(ENDPOINT + "/get_projects")
#     print(response.json())
#     assert response.status_code == 200
