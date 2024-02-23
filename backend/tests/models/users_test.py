from project.models.users import Users


class TestUserModel:
    """Test class for the database models"""

    def test_valid_user(self, db_session, valid_user):
        db_session.add(valid_user)
        db_session.commit()
        assert valid_user in db_session.query(Users).all()

    def test_is_teacher(self, db_session, teachers):
        db_session.add_all(teachers)
        db_session.commit()
        teacher_count = 0
        for usr in db_session.query(Users).filter_by(is_teacher=True):
            teacher_count += 1
            assert usr.is_teacher
        assert teacher_count == 10