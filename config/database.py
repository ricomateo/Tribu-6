import os

from sqlmodel import SQLModel, create_engine

sqlite_file_name = "../API_proyectos.sqlite"
base_dir = os.path.dirname(os.path.realpath(__file__))

DATABASE_URL = f"sqlite:///{os.path.join(base_dir,sqlite_file_name)}"

connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, echo=False, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
