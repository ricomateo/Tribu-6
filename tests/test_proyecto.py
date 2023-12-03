from fastapi.testclient import TestClient
from pytest_bdd import scenario, given, when, then
from datetime import date


ENDPOINT = "/projects"


@scenario("proyecto.feature", "The project is created successfully")
def test_create_project():
    pass


@given("the user declares the mandatory project data", target_fixture="project")
def create_project():
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
def validate_response(response):
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
    assert data["id"] == 1
    assert data["id"] is not None
    assert data["creation_date"] == date.today().strftime("%Y-%m-%d")
    assert data["end_date"] is None


# project1 = Projects(
#     name="Fix molinete",
#     state="Iniciado",
#     description="Arreglar los multiples problemas de software y hardware del molinete",
#     expected_duration_days=180,
#     project_leader_id=1,
# )


# def test_create_hero(client: TestClient):
#     response = client.get(ENDPOINT + "/get_projects")
#     app.dependency_overrides.clear()

#     assert response.status_code == 200


# from fastapi.testclient import TestClient

# from main import app


# client = TestClient(app)


# def test_read_item():
#     response = client.get(ENDPOINT + "/get_projects")
#     print(response.json())
#     assert response.status_code == 200
