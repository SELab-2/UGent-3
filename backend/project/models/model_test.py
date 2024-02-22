"""
To run this test make sure you are in the backend folder and run:
python -m unittest .\project\models\model_test.py  
"""

import unittest
import os
from sqlalchemy import create_engine
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
        # Create an in-memory SQLite database engine
        # Load environment variables from .env file
        load_dotenv()

        # Access the environment variables
        db_host = os.getenv('DB_HOST')
        engine = create_engine(db_host)

        # Create tables defined by your models
        db.metadata.create_all(engine)

        # Create a session for interacting with the database
        session = sessionmaker(bind=engine)
        self.session = session()


    def tearDown(self):
        # Flush and close the session
        self.session.expire_all()
        self.session.rollback()
        self.session.close()
        
        # Delete all data from each table
        for table in reversed(db.metadata.sorted_tables):
            self.session.execute(table.delete())

        # Commit the transaction
        self.session.commit()

    def test_users(self):
        """Test function for user model,
        first i simply test storing and retrieving a student,
        then i test if a query for only the teachers/admin works"""
        user = Users(uid="student", is_teacher=False, is_admin=False)

        # Add the user to the session
        self.session.add(user)

        # Commit the session to persist the user in the database
        self.session.commit()

        # Query the database for the user based on their uid
        retrieved_user = self.session.query(Users).filter_by(uid="student").first()

        # Assert that the retrieved user matches the one we created
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.uid, "student")
        self.assertEqual(retrieved_user.is_teacher, False)
        self.assertEqual(retrieved_user.is_admin, False)

        for i in range(10):
            user = Users(uid=str(i),is_teacher=True,is_admin=False)
            self.session.add(user)
            self.session.commit()
        teacher_count = 0
        for usr in self.session.query(Users).filter_by(is_teacher=True):
            teacher_count+=1
            self.assertTrue(usr.is_teacher)
        self.assertEqual(teacher_count,10)


if __name__ == "__main__":
    unittest.main()
