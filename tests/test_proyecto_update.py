from fastapi.testclient import TestClient
from pytest_bdd import scenario, given, when, then
from datetime import date

from sqlalchemy import exc


ENDPOINT = "/projects"


@scenario("proyecto_update.feature", "The project is edited successfully")
def test_update_project():
    pass


@given("the user has alredy created a project")
def create_project(client: TestClient):
    # Crear proyecto para despues actualizarlo
    response = client.post(
        ENDPOINT + "/create_project",
        json={
            "name": "Fix molinete",
            "state": "Iniciado",
            "description": "Arreglar los multiples problemas de software y hardware del molinete",
            "expected_duration_days": 180,
            "project_leader_id": 1,
        },
    )
    data = response.json()

    assert data["id"] == 1


@given("the user declares one or more project data", target_fixture="project")
def project_update_data():
    return {"state": "Finalizado", "end_date": date.today().strftime("%Y-%m-%d")}


@when("the user chooses to apply the changes to the project", target_fixture="response")
def send_post_update_project(project, client: TestClient):
    try:
        return client.patch(
            ENDPOINT + "/update_project/1",
            json=project,
        )
    except Exception as e:
        return e


@then("the new data is established and the user is informed")
def validate_update_succsessful(response):
    data = response.json()
    print(data)

    assert response.status_code == 200
    assert data["name"] == "Fix molinete"
    assert data["state"] == "Finalizado"
    assert (
        data["description"]
        == "Arreglar los multiples problemas de software y hardware del molinete"
    )
    assert data["expected_duration_days"] == 180
    assert data["project_leader_id"] == 1
    assert data["id"] is not None
    assert data["id"] == 1
    assert data["creation_date"] == date.today().strftime("%Y-%m-%d")
    assert data["end_date"] == date.today().strftime("%Y-%m-%d")


# --------------------------------------------------------------------------------------------------------------------#


@scenario("proyecto_update.feature", "Nulling a required field")
def test_nulling_required_field():
    pass


@given(
    "the user deletes one or more required data and leaves them without information",
    target_fixture="project",
)
def project_null_data():
    return {"name": None}


@then(
    "the user is  informed that it is not possible to apply the changes because there is missing data and is asked to complete them to edit the project"
)
def validate_update_null_required(response):
    print(response)
    assert type(response) == exc.IntegrityError
