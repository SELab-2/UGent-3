"""
To run this test make sure you are in the backend folder,
there is a .env file with DB_HOST set to a postgresql database 
that you have running locally and run:
python -m unittest .\project\models\model_test.py  
"""

import unittest
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from project import db
from project.models.courses import Courses
from project.models.course_relations import CourseAdmins, CourseStudents
from project.models.projects import Projects
from project.models.submissions import Submissions
from project.models.users import Users
from dotenv import load_dotenv


class TestModels(unittest.TestCase):
    """Test class for the database models"""

    def setUp(self):
        """
        Load the database uri and connect to it,
        then create the tables defined by the models
        and finally create a session so we can interact with the database
        """
        load_dotenv()
        db_host = os.getenv("DB_HOST")
        engine = create_engine(db_host)

        # Create tables defined by your models,
        # might want to change later since tables should already be defined in the database
        db.metadata.create_all(engine)

        session = sessionmaker(bind=engine)
        self.session = session()

    def tearDown(self):
        """
        Flush the whole test database and close the session
        """
        self.session.expire_all()
        self.session.rollback()
        self.session.close()

        for table in reversed(db.metadata.sorted_tables):
            self.session.execute(table.delete())
        self.session.commit()

    def test_users(self):
        """Test function for user model,
        first i simply test storing and retrieving a student,
        then i test if a query for only the teachers works"""
        user = Users(uid="student", is_teacher=False, is_admin=False)
        self.session.add(user)
        self.session.commit()  # only after commit the user will be in database

        retrieved_user = self.session.query(Users).filter_by(uid="student").first()

        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.uid, "student")
        self.assertEqual(retrieved_user.is_teacher, False)
        self.assertEqual(retrieved_user.is_admin, False)

        for i in range(10):
            user = Users(uid=str(i), is_teacher=True, is_admin=False)
            self.session.add(user)
            self.session.commit()
        teacher_count = 0
        for usr in self.session.query(Users).filter_by(is_teacher=True):
            teacher_count += 1
            self.assertTrue(usr.is_teacher)
        self.assertEqual(teacher_count, 10)

    def test_courses(self):
        """
        Test function for the courses model,
        i will create some users, students and teachers and i will connect them to some courses
        and then i will check if the queries work
        """

        sel2_teacher = Users(uid="teacher_sel2", is_teacher=True, is_admin=False)
        sel2 = Courses(name="Sel2", teacher=sel2_teacher.uid)

        with self.assertRaises(
            IntegrityError,
            msg="Courses should throw a foreign key error on the teacher uid",
        ):
            self.session.add(sel2)
            self.session.commit()
        self.session.rollback()

        self.session.add(sel2_teacher)
        self.session.commit()

        self.session.add(sel2)
        self.session.commit()
        self.assertEqual(
            self.session.query(Courses).filter_by(name="Sel2").first().teacher,
            sel2_teacher.uid,
        )

        students = [
            Users(uid="student_sel2_" + str(i), is_teacher=False, is_admin=False)
            for i in range(5)
        ]
        self.session.add_all(students)
        course_relations = [
            CourseStudents(course_id=sel2.course_id, uid=students[i].uid)
            for i in range(5)
        ]

        with self.assertRaises(
            IntegrityError,
            msg="Course_relations should throw a foreign key error on the student uid",
        ):
            self.session.add_all(course_relations)
            self.session.commit()
        self.session.rollback()

        self.session.add_all(students)
        self.session.commit()
        self.session.add_all(course_relations)
        self.session.commit()

        student_check = [
            s.uid
            for s in self.session.query(CourseStudents)
            .filter_by(course_id=sel2.course_id)
            .all()
        ]
        student_uids = [s.uid for s in students]
        self.assertListEqual(student_check, student_uids)

        assistent = Users(uid="assistent_sel2")
        self.session.add(assistent)
        self.session.commit()

        admin_relation = CourseAdmins(uid=assistent.uid, course_id=sel2.course_id)
        self.session.add(admin_relation)
        self.session.commit()

        self.assertEqual(
            self.session.query(CourseAdmins)
            .filter_by(course_id=sel2.course_id)
            .first()
            .uid,
            assistent.uid,
        )

    def test_projects_and_submissions(self):
        """
        In this test function i will test the
        creation of projects and submissions
        """

        teacher = Users(uid="teacher", is_teacher=True)
        self.session.add(teacher)
        self.session.commit()
        course = Courses(name="course", teacher=teacher.uid)
        self.session.add(course)
        self.session.commit()
        deadline = datetime(2024, 2, 25, 12, 0, 0)  # February 25, 2024, 12:00 PM
        project = Projects(
            title="Project",
            descriptions="Test project",
            deadline=deadline,
            course_id=course.course_id,
            visible_for_students=True,
            archieved=False,
        )

        self.session.add(project)
        self.session.commit()

        check_project = (
            self.session.query(Projects).filter_by(title=project.title).first()
        )
        self.assertEqual(check_project.deadline, project.deadline)

        submittor = Users(uid="student")
        self.assertFalse(submittor.is_teacher)
        self.session.add(submittor)
        self.session.commit()

        submission = Submissions(
            uid=submittor.uid,
            project_id=check_project.project_id,
            submission_time=datetime.now(),
            submission_path="/test/submission/",
            submission_status=False,
        )
        self.session.add(submission)
        self.session.commit()

        submission_check = (
            self.session.query(Submissions)
            .filter_by(project_id=check_project.project_id)
            .first()
        )
        self.assertEqual(submission_check.uid, submittor.uid)
        with self.assertRaises(
            IntegrityError,
            msg="Submissions model should throw an error on grades out of [0,20] range",
        ):
            submission_check.grading = 100
            self.session.commit()
        self.session.rollback()

        submission_check.grading = 15
        self.session.commit()

        submission_check = (
            self.session.query(Submissions)
            .filter_by(project_id=check_project.project_id)
            .first()
        )
        self.assertEqual(submission_check.grading, 15)
        self.assertEqual(
            submission.grading, 15
        )  # Interesting! all the model objects are connected


if __name__ == "__main__":
    unittest.main()
