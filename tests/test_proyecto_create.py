from fastapi.testclient import TestClient
from pytest_bdd import scenario, given, when, then
from datetime import date


ENDPOINT = "/projects"


@scenario("proyecto_create.feature", "The project is created successfully")
def test_create_project():
    pass


@given("the user declares the mandatory project data", target_fixture="project")
def project_full_data():
    return {
        "name": "Fix molinete",
        "state": "Iniciado",
        "description": "Arreglar los multiples problemas de software y hardware del molinete",
        "expected_duration_days": 180,
        "project_leader_id": 1,
    }


@when(
    "the user chooses to confirm the creation of the project", target_fixture="response"
)
def send_post_create_project(project, client: TestClient):
    return client.post(
        ENDPOINT + "/create_project",
        json=project,
    )


@then("the project is created with the previously loaded data and the user is informed")
def validate_response_complete(response):
    data = response.json()
    print(data)

    assert response.status_code == 201
    assert data["name"] == "Fix molinete"
    assert data["state"] == "Iniciado"
    assert (
        data["description"]
        == "Arreglar los multiples problemas de software y hardware del molinete"
    )
    assert data["expected_duration_days"] == 180
    assert data["project_leader_id"] == 1
    assert data["id"] is not None
    # assert data["id"] == 1
    assert data["creation_date"] == date.today().strftime("%Y-%m-%d")
    assert data["end_date"] is None


# --------------------------------------------------------------------------------------------------------------------#


@scenario("proyecto_create.feature", "Missing data")
def test_missing_data():
    pass


@given(
    "the user omits at least one of the project's required data",
    target_fixture="project",
)
def project_missing_data():
    return {
        "name": "Fix molinete",
        # falta state
        "description": "Arreglar los multiples problemas de software y hardware del molinete",
        "expected_duration_days": 180,
        "project_leader_id": 1,
    }


@then(
    "the user is informed that there is missing data and is asked to complete it to successfully create the project"
)
def validate_response_missing_data(response):
    data = response.json()
    print(data)

    assert response.status_code == 422
    assert data["detail"][0]["msg"] == "field required"
    assert data["detail"][0]["loc"] == ["body", "state"]


# --------------------------------------------------------------------------------------------------------------------#


@scenario("proyecto_create.feature", "A project with the same name already exists")
def test_same_name():
    pass


@given("the declared name is the same as the name of an existing project")
def create_project_same_name(client: TestClient):
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

    assert response.status_code == 201
    assert data["name"] == "Fix molinete"
    assert data["state"] == "Iniciado"
    assert (
        data["description"]
        == "Arreglar los multiples problemas de software y hardware del molinete"
    )
    assert data["expected_duration_days"] == 180
    assert data["project_leader_id"] == 1
    assert data["id"] is not None
    assert data["creation_date"] == date.today().strftime("%Y-%m-%d")
    assert data["end_date"] is None


# --------------------------------------------------------------------------------------------------------------------#


@scenario("proyecto_create.feature", "Wrong proyect leader id")
def test_leader_id():
    pass


@given(
    "the user declares the wrong project leader id",
    target_fixture="project",
)
def project_wrong_leader_id():
    return {
        "name": "Fix molinete",
        "state": "Iniciado",
        "description": "Arreglar los multiples problemas de software y hardware del molinete",
        "expected_duration_days": 180,
        "project_leader_id": 0,  # No hay empleado con ese id
    }


@then(
    "the user is informed that there is no employee with that id and is asked to correct it to successfully create the project"
)
def validate_response_wrong_leader_id(response):
    data = response.json()
    print(data)

    assert response.status_code == 404
    assert data["detail"] == "No hay empleado con ese legajo"
