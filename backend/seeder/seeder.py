"""Seeder file does the actual seeding of the db"""
import argparse
import os
import random
import string
from datetime import datetime, timedelta

from dotenv import load_dotenv
from faker import Faker
from faker.providers import DynamicProvider
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils import register_composites

from project.models.course import Course
from project.models.course_relation import CourseAdmin, CourseStudent
from project.models.project import Project
from project.models.submission import Submission, SubmissionStatus
from project.models.user import User
from project.sessionmaker import Session as session_maker

load_dotenv()

UPLOAD_URL = os.getenv("UPLOAD_FOLDER")

fake = Faker()

# Get the directory of the current script
script_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the path to titles.txt relative to the script directory
titles_path = os.path.join(script_dir, 'titles.txt')

with open(titles_path, 'r', encoding='utf-8') as file:
    # Read the lines of the file and strip newline characters
    titles = [line.strip() for line in file]

course_title_provider = DynamicProvider(  # Custom course titles.
    provider_name="course_titles",
    elements=titles,
)
fake.add_provider(course_title_provider)


def generate_course_name():
    """Generates a course name chosen from the predefined provider"""
    return fake.course_titles()


def generate_random_uid(length=8):
    """Generates a random uid of given length"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def teacher_generator():
    """Generates a teacher user object"""
    return user_generator('TEACHER')


def student_generator():
    """Generates a student user object"""
    return user_generator('STUDENT')


def admin_generator():
    """Generates an admin user object"""
    return user_generator('ADMIN')


def user_generator(role):
    """Generates a user object with the given role"""
    user = User(uid=generate_random_uid(),
                role=role,
                display_name=fake.name())
    return user


def course_student_generator(course_id, uid):
    """Generates a course student relation object"""
    return CourseStudent(course_id=course_id, uid=uid)


def course_admin_generator(course_id, uid):
    """Generates a course admin relation object"""
    return CourseAdmin(course_id=course_id, uid=uid)


def generate_course(teacher_uid):
    """Generates a course object with a random name and the given teacher uid"""
    course = Course(name=generate_course_name(),
                    teacher=teacher_uid)
    return course


def generate_projects(course_id, num_projects):
    """Generates a list of project objects with random future deadlines"""
    projects = []
    for _ in range(num_projects):
        deadlines = []
        # Generate a random number of deadlines (0-2)
        num_deadlines = random.randint(0, 2)

        for _ in range(num_deadlines):
            if random.random() < 1/3:
                past_datetime = datetime.now() - timedelta(days=random.randint(1, 30))
                deadline = (fake.catch_phrase(), past_datetime)
            else:
                future_datetime = datetime.now() + timedelta(days=random.randint(1, 30))
                deadline = (fake.catch_phrase(), future_datetime)
            deadlines.append(deadline)
        project = Project(
            title=fake.catch_phrase(),
            description=fake.catch_phrase(),
            deadlines=deadlines,
            course_id=course_id,
            visible_for_students=random.choice([True, False]),
            archived=random.choice([True, False]),
            regex_expressions=[]
        )
        projects.append(project)
    return projects


def generate_submissions(project_id, student_uid):
    """Generates a list of submissions with random status"""
    submissions = []
    statusses = [SubmissionStatus.SUCCESS, SubmissionStatus.FAIL,
                 SubmissionStatus.LATE, SubmissionStatus.RUNNING]
    num_submissions = random.randint(0, 2)
    submission_times = []
    for _ in range(num_submissions):
        past_datetime = datetime.now() - timedelta(days=random.randint(0, 10))
        while past_datetime in submission_times:
            past_datetime = datetime.now() - timedelta(days=random.randint(0, 10))
        submission_times.append(past_datetime)
        submission = Submission(project_id=project_id,
                                uid=student_uid,
                                submission_time=past_datetime,
                                submission_path="",
                                submission_status=random.choice(statusses))
        graded = random.choice([True, False])
        if graded and submission.submission_status == "SUCCESS":
            submission.grading = random.randint(0, 20)
        submissions.append(submission)
    return submissions


def into_the_db(my_uid):
    """Populates the db with 5 courses where my_uid is teacher and 5 where he is student"""
    try:
        session = session_maker()  # setup the db session
        connection = session.connection()
        register_composites(connection)

        students = []
        # make a random amount of 100-200 students which we can use later to populate courses
        num_students = random.randint(100, 200)
        students = [student_generator() for _ in range(num_students)]
        session.add_all(students)
        session.commit()

        num_teachers = random.randint(5, 10)
        teachers = [teacher_generator() for _ in range(num_teachers)]
        session.add_all(teachers)
        session.commit()  # only after commit uid becomes available

        for _ in range(5):  # 5 courses where my_uid is teacher
            course_id = insert_course_into_db_get_id(session, my_uid)
            # Add students to the course
            subscribed_students = populate_course_students(
                session, course_id, students)
            populate_course_projects(
                session, course_id, subscribed_students)

        for _ in range(5):  # 5 courses where my_uid is a student
            teacher_uid = teachers[random.randint(0, len(teachers)-1)].uid
            course_id = insert_course_into_db_get_id(session, teacher_uid)
            subscribed_students = populate_course_students(
                session, course_id, students)
            session.add(CourseStudent(course_id=course_id, uid=my_uid))
            session.commit()
            subscribed_students.append(my_uid)  # my_uid is also a student
            populate_course_projects(
                session, course_id, subscribed_students)
    except SQLAlchemyError as e:
        if session:  # possibly error resulted in session being null
            session.rollback()
        raise e
    finally:
        session.close()


def insert_course_into_db_get_id(session, teacher_uid):
    """Inserts a course with teacher_uid as teacher into the db and returns the course_id"""
    course = generate_course(teacher_uid)
    session.add(course)
    session.commit()
    return course.course_id


def populate_course_students(session, course_id, students):
    """Populates the course with students and returns their uids as a list"""
    num_students_in_course = random.randint(5, 30)
    subscribed_students = random.sample(students, num_students_in_course)
    student_relations = [course_student_generator(course_id, student.uid)
                            for student in subscribed_students]

    session.add_all(student_relations)
    session.commit()

    return [student.uid for student in subscribed_students]


def populate_course_projects(session, course_id, students):
    """Populates the course with projects and submissions, also creates the files"""
    num_projects = random.randint(1, 3)
    projects = generate_projects(course_id, num_projects)
    session.add_all(projects)
    session.commit()
    for project in projects:
        project_id = project.project_id
        # Write assignment.md file
        assignment_content = fake.text()
        assignment_file_path = os.path.join(
            UPLOAD_URL, str(project_id), "assignment.md")
        os.makedirs(os.path.dirname(assignment_file_path), exist_ok=True)
        with open(assignment_file_path, "w", encoding="utf-8") as assignment_file:
            assignment_file.write(assignment_content)
        populate_project_submissions(session, students, project_id)


def populate_project_submissions(session, students, project_id):
    """Make submissions, 0 1 or 2 for each project per student"""
    for student in students:
        submissions = generate_submissions(project_id, student)
        session.add_all(submissions)
        session.commit()
        for submission in submissions:
            submission_directory = os.path.join(UPLOAD_URL, str(
                project_id), "submissions", str(submission.submission_id), "submission")
            os.makedirs(submission_directory, exist_ok=True)
            submission_file_path = os.path.join(
                submission_directory, "submission.md")
            with open(submission_file_path, "w", encoding="utf-8") as submission_file:
                submission_file.write(fake.text())

            submission.submission_path = submission_directory
            session.commit()  # update submission path

# Create a function to parse command line arguments
def parse_args():
    """Parse the given uid from the command line"""
    parser = argparse.ArgumentParser(description='Populate the database')
    parser.add_argument('my_uid', type=str, help='Your UID')
    return parser.parse_args()

# Main function to run when script is executed
def main():
    """Parse arguments, pass them to into_the_db function"""
    args = parse_args()
    into_the_db(args.my_uid)

if __name__ == '__main__':
    main()
