from fastapi.testclient import TestClient
from pytest_bdd import scenario, given, when, then
from datetime import date


ENDPOINT = "/projects"


@scenario("proyecto_delete.feature", "The project is successfully deleted")
def test_delete_present_project():
    pass


@given("there are projects created")
def created_projects(client: TestClient):
    response1 = client.post(
        ENDPOINT + "/create_project",
        json={
            "name": "Fix molinete",
            "state": "Iniciado",
            "description": "Arreglar los multiples problemas de software y hardware del molinete",
            "expected_duration_days": 180,
            "project_leader_id": 1,
        },
    )
    data1 = response1.json()

    assert data1["id"] == 1

    response2 = client.post(
        ENDPOINT + "/create_project",
        json={
            "name": "Update molinete",
            "state": "No iniciado",
            "description": "Agregar nuevas funcionalidades",
            "expected_duration_days": 100,
            "project_leader_id": 2,
        },
    )
    data2 = response2.json()

    assert data2["id"] == 2


@when("the user chooses to delete a project", target_fixture="response")
def send_delete_project(client: TestClient):
    return client.delete(ENDPOINT + "/delete_project/2")


@when("confirm the deletion of the project")
def confirm_delete_project(response):
    data = response.json()

    assert data["name"] == "Update molinete"
    assert data["state"] == "No iniciado"
    assert data["description"] == "Agregar nuevas funcionalidades"
    assert data["expected_duration_days"] == 100
    assert data["project_leader_id"] == 2
    assert data["id"] == 2
    assert data["creation_date"] == date.today().strftime("%Y-%m-%d")
    assert data["end_date"] is None


@then("the project is deleted and is no longer shown in the project list")
def validate_project_deletion(client: TestClient):
    response_get = client.get(ENDPOINT + "/get_projects")

    data = response_get.json()
    print(data)

    assert response_get.status_code == 200
    assert data[0]["name"] == "Fix molinete"
    assert data[0]["state"] == "Iniciado"
    assert (
        data[0]["description"]
        == "Arreglar los multiples problemas de software y hardware del molinete"
    )
    assert data[0]["expected_duration_days"] == 180
    assert data[0]["project_leader_id"] == 1
    assert data[0]["id"] == 1
    assert data[0]["creation_date"] == date.today().strftime("%Y-%m-%d")
    assert data[0]["end_date"] is None
