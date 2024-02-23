from project.models.users import Users


class TestModels:
    """Test class for the database models"""

    def test_valid_user(self, db_session, valid_user):
        db_session.add(valid_user)
        db_session.commit()
        assert valid_user in db_session.query(Users).all()