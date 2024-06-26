"""User model tests"""

from pytest import raises, mark
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from project.models.user import User,Role

class TestUserModel:
    """Class to test the User model"""

    def test_create_user(self, session: Session):
        """Test if a user can be created"""
        user = User(uid="user01", role=Role.STUDENT)
        session.add(user)
        session.commit()
        assert session.get(User, "user01") is not None
        assert session.query(User).count() == 12

    def test_query_user(self, session: Session):
        """Test if a user can be queried"""
        assert session.query(User).count() == 11
        teacher = session.query(User).filter_by(uid="brinkmann").first()
        assert teacher is not None
        assert teacher.role == Role.ADMIN

    def test_update_user(self, session: Session):
        """Test if a user can be updated"""
        student = session.query(User).filter_by(uid="student01").first()
        student.role = Role.ADMIN
        session.commit()
        assert session.get(User, "student01").role == Role.ADMIN

    def test_delete_user(self, session: Session):
        """Test if a user can be deleted"""
        user = session.query(User).first()
        session.delete(user)
        session.commit()
        assert session.get(User, user.uid) is None
        assert session.query(User).count() == 10

    @mark.parametrize("property_name", ["uid"])
    def test_property_not_nullable(self, session: Session, property_name: str):
        """Test if the property is not nullable"""
        user = session.query(User).first()
        with raises(IntegrityError):
            setattr(user, property_name, None)
            session.commit()
        session.rollback()

    @mark.parametrize("property_name", ["uid"])
    def test_property_unique(self, session: Session, property_name: str):
        """Test if the property is unique"""
        users = session.query(User).all()
        with raises(IntegrityError):
            setattr(users[0], property_name, getattr(users[1], property_name))
            session.commit()
        session.rollback()
