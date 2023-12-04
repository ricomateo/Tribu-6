from fastapi.testclient import TestClient
from pytest_bdd import scenario, given, when, then
from datetime import date


ENDPOINT = "/tasks"


@scenario("tarea_read.feature", "Tasks are displayed successfully")
def test_consult_present_tasks():
    pass


@given("the project has tasks")
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


@when("the user chooses to consult the project tasks", target_fixture="response")
def send_get_tasks(client: TestClient):
    return client.get(ENDPOINT + "/get_tasks")


@then("you are shown a list of all the tasks")
def validate_get_succsessful(response):
    data = response.json()
    print(data)

    assert response.status_code == 200

    # Primer tarea
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

    # Segunda tarea

    assert data[1]["name"] == "Fix login web"
    assert data[1]["state"] == "Iniciado"
    assert data[1]["priority"] == "Media"
    assert (
        data[1]["description"]
        == "Arreglar problema cuando usuario se quiere loguear en la pagina"
    )
    assert data[1]["project_id"] == 1
    assert data[1]["responsible_id"] == 2
    assert data[1]["id"] == 2
    assert data[1]["creation_date"] == date.today().strftime("%Y-%m-%d")
    assert data[1]["end_date"] is None


# -------------------------------------------------------------------------------------------------------------------#


@scenario("tarea_read.feature", "No tasks to display")
def test_consult_no_tasks():
    pass


@given("the project has no tasks")
def no_created_tasks():
    # ¯\_(ツ)_/¯
    pass


@then("you are informed that the project has no tasks")
def validate_get_no_tasks(response):
    data = response.json()
    print(data)

    # Primer tarea
    assert response.status_code == 200
    assert data == []
