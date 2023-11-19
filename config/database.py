import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqlite_file_name = "../area_proyectos.sqlite"
base_dir = os.path.dirname(os.path.realpath(__file__))

DATABASE_URL = f"sqlite:///{os.path.join(base_dir,sqlite_file_name)}"

engine = create_engine(
    DATABASE_URL, echo=False
)  # connect_args={"check_same_thread": False}

Session = sessionmaker(bind=engine)  # autoflush=False

Base = declarative_base()
