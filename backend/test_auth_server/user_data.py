import dataclasses

from sqlalchemy import Boolean, Column, String
from test_auth_server.db_in import db

@dataclasses.dataclass
class User_data(db.Model):

    __tablename__ = "user_data"
    access_token:str= Column(String(255), primary_key=True)
    id:str = Column(String(255))
    jobCategory:str = Column(String(255), nullable=True)