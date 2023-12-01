from typing import Optional

from sqlmodel import Field, SQLModel


class EmployeesBase(SQLModel):
    name: str
    last_name: str


class Employees(EmployeesBase, table=True):
    legajo: Optional[int] = Field(default=None, primary_key=True)


# class EmployeesCreate(EmployeesBase):
#     pass


class EmployeesRead(EmployeesBase):
    legajo: int


# class EmployeesUpdate(SQLModel):
#     name: Optional[str] = None
#     last_name: Optional[str] = None
