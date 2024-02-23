"""
To run this test make sure you are in the backend folder and run:
python -m unittest .\project\models\model_test.py  
"""

import unittest
import os
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


if __name__ == "__main__":
    unittest.main()
