from fastapi.testclient import TestClient
from pytest_bdd import scenario, given, when, then
from datetime import date


ENDPOINT = "/tasks"


@scenario("tarea_create.feature", "Task is created successfully")
def test_create_task():
    pass


@given("the user declares the required task data", target_fixture="task")
def task_full_data(client: TestClient):
    # Crear proyecto para que no de error crear una tarea sin un project_id correcto
    response = client.post(
        "projects/create_project",
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
    assert data["id"] == 1

    return {
        "name": "Fix login app",
        "state": "Iniciado",
        "priority": "Alta",
        "description": "Arreglar problema cuando usuario se quiere loguear con la app",
        "project_id": 1,
        "responsible_id": 1,
    }


@when("the user chooses to confirm the creation of the task", target_fixture="response")
def send_post_create_task(task, client: TestClient):
    return client.post(
        ENDPOINT + "/create_task",
        json=task,
    )


@then("the task is added to the project successfully and the user is informed")
def validate_response_complete(response):
    data = response.json()
    print(data)

    assert response.status_code == 201
    assert data["name"] == "Fix login app"
    assert data["state"] == "Iniciado"
    assert data["priority"] == "Alta"
    assert (
        data["description"]
        == "Arreglar problema cuando usuario se quiere loguear con la app"
    )
    assert data["project_id"] == 1
    assert data["responsible_id"] == 1
    assert data["id"] is not None
    assert data["creation_date"] == date.today().strftime("%Y-%m-%d")
    assert data["end_date"] is None


# --------------------------------------------------------------------------------------------------------------------#


@scenario("tarea_create.feature", "Missing data")
def test_missing_data():
    pass


@given(
    "the user omits at least one of the required task data",
    target_fixture="task",
)
def task_missing_data(client: TestClient):
    # Crear proyecto para que no de error crear una tarea sin un project_id correcto
    response = client.post(
        "projects/create_project",
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
    assert data["id"] == 1

    return {
        "name": "Fix login app",
        # Falta state
        "priority": "Alta",
        "description": "Arreglar problema cuando usuario se quiere loguear con la app",
        "project_id": 1,
        "responsible_id": 1,
    }


@then(
    "the user is informed that there is missing data and is prompted to complete it to successfully create the task"
)
def validate_response_missing_data(response):
    data = response.json()
    print(data)

    assert response.status_code == 422
    assert data["detail"][0]["msg"] == "field required"
    assert data["detail"][0]["loc"] == ["body", "state"]


# --------------------------------------------------------------------------------------------------------------------#


@scenario("tarea_create.feature", "A task with that name already exists")
def test_same_name():
    pass


@given("the declared name is the same as the name of an existing task in the project")
def create_task_same_name(client: TestClient):
    response = client.post(
        ENDPOINT + "/create_task",
        json={
            "name": "Fix login app",
            "state": "Iniciado",
            "priority": "Alta",
            "description": "Arreglar problema cuando usuario se quiere loguear con la app",
            "project_id": 1,
            "responsible_id": 1,
        },
    )

    data = response.json()

    assert response.status_code == 201
    assert data["name"] == "Fix login app"
    assert data["state"] == "Iniciado"
    assert data["priority"] == "Alta"
    assert (
        data["description"]
        == "Arreglar problema cuando usuario se quiere loguear con la app"
    )
    assert data["project_id"] == 1
    assert data["responsible_id"] == 1
    assert data["id"] == 1
    assert data["creation_date"] == date.today().strftime("%Y-%m-%d")
    assert data["end_date"] is None
