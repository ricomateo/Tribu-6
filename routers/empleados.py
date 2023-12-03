import requests
from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlmodel import Session, select
from models.empleados import Employees, EmployeesRead
from config.database import engine, get_session

routerEmployees = APIRouter(
    prefix="/employees",
    tags=["Employees"],
    responses={404: {"description": "Not found"}},
)


@routerEmployees.get(
    "/get_employees", status_code=status.HTTP_200_OK, response_model=List[EmployeesRead]
)
def get_employees(*, session: Session = Depends(get_session)):
    employees = session.exec(select(Employees)).all()
    return employees


@routerEmployees.get(
    "/get_employee/{id}",
    status_code=status.HTTP_200_OK,
    response_model=Employees,
)
def get_employee_by_id(*, session: Session = Depends(get_session), id: int):
    employee = session.get(Employees, id)
    if not employee:
        raise HTTPException(status_code=404, detail="No se encontro tarea")

    return employee


def create_employees_from_API():
    """
    Si está vacia, agrega los empleados, a partir del endpoint dado en clase, a la base de datos
    """
    with Session(engine) as session:
        if not session.exec(select(Employees)).all():
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
