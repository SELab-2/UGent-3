"""

"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from project import db
from project.models.users import Users
from sqlalchemy.engine.url import URL
from dotenv import load_dotenv
import pytest

load_dotenv()

DATABSE_NAME = os.getenv('POSTGRES_DB')
DATABASE_USER = os.getenv('POSTGRES_USER')
DATABASE_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DATABASE_HOST = os.getenv('POSTGRES_HOST')

url = URL.create(
    drivername="postgresql",
    username=DATABASE_USER,
    host=DATABASE_HOST,
    database=DATABSE_NAME,
    password=DATABASE_PASSWORD
)

engine = create_engine(url)
Session = sessionmaker(bind=engine)

@pytest.fixture
def db_session():
    db.metadata.create_all(engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def valid_user():
    user = Users(uid="student", is_teacher=False, is_admin=False)
    return user
