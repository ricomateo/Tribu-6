from fastapi.testclient import TestClient
from pytest_bdd import scenario, given, when, then
from datetime import date


ENDPOINT = "/tasks"


@scenario("tarea_delete.feature", "Task is deleted successfully")
def test_delete_present_task():
    pass


@given("there are tasks created within a project")
def created_tasks(client: TestClient):
    # Crear proyecto para que no de error crear una tarea sin un project_id correcto
    response_project = client.post(
        "projects/create_project",
        json={
            "name": "Fix molinete",
            "state": "Iniciado",
            "description": "Arreglar los multiples problemas de software y hardware del molinete",
            "expected_duration_days": 180,
            "project_leader_id": 1,
        },
    )
    data_project = response_project.json()
    assert response_project.status_code == 201
    assert data_project["id"] == 1

    # Crear tareas
    response_task1 = client.post(
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

    data_task1 = response_task1.json()

    assert response_task1.status_code == 201
    assert data_task1["id"] == 1

    response_task2 = client.post(
        ENDPOINT + "/create_task",
        json={
            "name": "Fix login web",
            "state": "Iniciado",
            "priority": "Media",
            "description": "Arreglar problema cuando usuario se quiere loguear en la pagina",
            "project_id": 1,
            "responsible_id": 2,
        },
    )

    data_task2 = response_task2.json()

    assert response_task2.status_code == 201
    assert data_task2["id"] == 2


@when("the user chooses to delete a task", target_fixture="response")
def send_delete_task(client: TestClient):
    return client.delete(ENDPOINT + "/delete_task/2")


@when("confirm the deletion of the task")
def confirm_delete_task(response):
    data = response.json()

    assert data["name"] == "Fix login web"
    assert data["state"] == "Iniciado"
    assert data["priority"] == "Media"
    assert (
        data["description"]
        == "Arreglar problema cuando usuario se quiere loguear en la pagina"
    )
    assert data["project_id"] == 1
    assert data["responsible_id"] == 2
    assert data["id"] == 2
    assert data["creation_date"] == date.today().strftime("%Y-%m-%d")
    assert data["end_date"] is None


@then("the task is deleted and is no longer shown in the project task list")
def validate_task_deletion(client: TestClient):
    response_get = client.get(ENDPOINT + "/get_tasks")

    data = response_get.json()
    print(data)

    assert response_get.status_code == 200
    assert data[0]["name"] == "Fix login app"
    assert data[0]["state"] == "Iniciado"
    assert data[0]["priority"] == "Alta"
    assert (
        data[0]["description"]
        == "Arreglar problema cuando usuario se quiere loguear con la app"
    )
    assert data[0]["project_id"] == 1
    assert data[0]["responsible_id"] == 1
    assert data[0]["id"] == 1
    assert data[0]["creation_date"] == date.today().strftime("%Y-%m-%d")
    assert data[0]["end_date"] is None
