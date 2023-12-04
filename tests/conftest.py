import sys

sys.path.append("../Tribu-6")

import pytest
import requests
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app
from config.database import get_session
from models.empleados import Employees


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        employees_json = requests.get(
            "https://anypoint.mulesoft.com/mocking/api/v1/sources/exchange/assets/754f50e8-20d8-4223-bbdc-56d50131d0ae/recursos-psa/1.0.0/m/api/recursos"
        ).json()

        for employee in employees_json:
            employee_db = Employees(
                name=employee["Nombre"],
                last_name=employee["Apellido"],
                legajo=employee["legajo"],
            )
            session.add(employee_db)

        session.commit()

        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
