"""initialise a datab session"""
from os import getenv
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker

url = URL.create(
    drivername="postgresql",
    username=getenv("POSTGRES_USER"),
    password=getenv("POSTGRES_PASSWORD"),
    host=getenv("POSTGRES_HOST"),
    database=getenv("POSTGRES_DB")
)

engine = create_engine(url)
Session = sessionmaker(bind=engine)