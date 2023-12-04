from fastapi.testclient import TestClient
from pytest_bdd import scenario, given, when, then
from datetime import date

from sqlalchemy import exc


ENDPOINT = "/tasks"


@scenario("tarea_update.feature", "The task is edited successfully")
def test_update_task():
    pass


@given("there are already projects and tasks created")
def create_task(client: TestClient):
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

    # Crear tarea para despues actualizarlo
    response_task = client.post(
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

    data_task = response_task.json()

    assert response_task.status_code == 201
    assert data_task["id"] == 1


@given("the user declares one or more task data", target_fixture="task")
def task_update_data():
    return {"state": "Finalizado", "end_date": date.today().strftime("%Y-%m-%d")}


@when("the user chooses to apply the changes", target_fixture="response")
def send_post_update_task(task, client: TestClient):
    try:
        return client.patch(
            ENDPOINT + "/update_task/1",
            json=task,
        )
    except Exception as e:
        return e


@then("the new data is established and the user is informed")
def validate_update_succsessful(response):
    data = response.json()
    print(data)

    assert response.status_code == 200
    assert data["name"] == "Fix login app"
    assert data["state"] == "Finalizado"
    assert data["priority"] == "Alta"
    assert (
        data["description"]
        == "Arreglar problema cuando usuario se quiere loguear con la app"
    )
    assert data["project_id"] == 1
    assert data["responsible_id"] == 1
    assert data["id"] == 1
    assert data["creation_date"] == date.today().strftime("%Y-%m-%d")
    assert data["end_date"] == date.today().strftime("%Y-%m-%d")


# --------------------------------------------------------------------------------------------------------------------#


@scenario("tarea_update.feature", "Nulling a required field")
def test_nulling_required_field():
    pass


@given(
    "the user deletes one or more mandatory data from the task and leaves them without information",
    target_fixture="task",
)
def task_null_data():
    return {"name": None}


@then(
    "the user is informed that the changes cannot be applied because there is missing data and is asked to complete them to edit the task"
)
def validate_update_null_required(response):
    print(response)
    assert type(response) == exc.IntegrityError
