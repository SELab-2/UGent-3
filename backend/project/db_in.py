"""db initialization"""

import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import URL

db = SQLAlchemy()
load_dotenv()

DATABSE_NAME = os.getenv("POSTGRES_DB")
DATABASE_USER = os.getenv("POSTGRES_USER")
DATABASE_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DATABASE_HOST = os.getenv("POSTGRES_HOST")

url = URL.create(
    drivername="postgresql",
    username=DATABASE_USER,
    host=DATABASE_HOST,
    database=DATABSE_NAME,
    password=DATABASE_PASSWORD,
)
