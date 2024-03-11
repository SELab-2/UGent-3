"""User model tests"""

from sqlalchemy.orm import Session
from project.models.user import User

class TestUserModel:
    """Class to test the User model"""

    def test_create_user(self, session: Session):
        """Test if a user can be created"""
        user = User(uid="user01", is_teacher=False, is_admin=False)
        session.add(user)
        session.commit()
        assert session.get(User, "user01") is not None

    def test_query_user(self, session: Session):
        """Test if a user can be queried"""
        assert session.query(User).count() == 4

        teacher = session.query(User).filter_by(uid="brinkmann").first()
        assert teacher is not None
        assert teacher.is_teacher

    def test_update_user(self, session: Session):
        """Test if a user can be updated"""
        student = session.query(User).filter_by(uid="student01").first()
        student.is_admin = True
        session.commit()
        assert session.get(User, "student01").is_admin

    def test_delete_user(self, session: Session):
        """Test if a user can be deleted"""
