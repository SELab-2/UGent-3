"""Tests for the Group and GroupStudent model"""
from sqlalchemy.orm import Session

from project.models.project import Project
from project.models.group import Group
from project.models.group_student import GroupStudent
from project.models.user import User


class TestGroupModel:
    """Test class for Group and GroupStudent tests"""

    def test_group_model(self, session: Session):
        "Group create test"
        project = session.query(Project).first()
        group = Group(project_id=project.project_id, group_size=4)
        session.add(group)
        session.commit()
        assert session.query(Group).filter_by(
            group_id=group.group_id, project_id=project.project_id) is not None
        assert session.query(Group).first().group_size == 4

    def test_group_join(self, session: Session):
        """Group join test"""
        project = session.query(Project).filter_by(title="B+ Trees").first()
        group = session.query(Group).filter_by(
            project_id=project.project_id).first()
        student = session.query(User).first()

        student_group = GroupStudent(
            group_id=group.group_id, uid=student.uid, project_id=project.project_id)
        session.add(student_group)
        session.commit()
        assert session.query(GroupStudent).first().uid == student.uid

    def test_group_leave(self, session: Session):
        """Group leave test"""
        project = session.query(Project).filter_by(title="B+ Trees").first()
        group = session.query(Group).filter_by(
            project_id=project.project_id).first()
        student = session.query(User).first()

        student_group = GroupStudent(
            group_id=group.group_id, uid=student.uid, project_id=project.project_id)
        session.add(student_group)
        session.commit()

        session.delete(student_group)
        session.commit()

        assert session.query(GroupStudent).filter_by(
            uid=student.uid, group_id=group.group_id, project_id=project.project_id).first() is None
