from fastapi.testclient import TestClient
from pytest_bdd import scenario, given, when, then
from datetime import date

from sqlalchemy import exc


ENDPOINT = "/projects"


@scenario("proyecto_read.feature", "There are projects")
def test_consult_present_projects():
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


@when("the user chooses to consult the projects", target_fixture="response")
def send_get_projects(client: TestClient):
    return client.get(ENDPOINT + "/get_projects")


@then("you are shown a list of all the projects")
def validate_get_succsessful(response):
    data = response.json()
    print(data)

    # Primer proyecto
    assert response.status_code == 200
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

    # Segundo proyecto
    assert data[1]["name"] == "Update molinete"
    assert data[1]["state"] == "No iniciado"
    assert data[1]["description"] == "Agregar nuevas funcionalidades"
    assert data[1]["expected_duration_days"] == 100
    assert data[1]["project_leader_id"] == 2
    assert data[1]["id"] == 2
    assert data[1]["creation_date"] == date.today().strftime("%Y-%m-%d")
    assert data[1]["end_date"] is None


# -------------------------------------------------------------------------------------------------------------------#


@scenario("proyecto_read.feature", "No projects created")
def test_consult_no_projects():
    pass


@given("there are no projects created")
def no_created_projects():
    # ¯\_(ツ)_/¯
    pass


@then("you are informed that there are no projects yet")
def validate_get_no_projects(response):
    data = response.json()
    print(data)

    # Primer proyecto
    assert response.status_code == 200
    assert data == []
