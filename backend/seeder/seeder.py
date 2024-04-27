from project.models.user import User
from project.models.course import Course
from project.models.project import Project
from project.models.course_relation import CourseStudent, CourseAdmin
from project.models.submission import Submission, SubmissionStatus
import random
import string
from .elements import course_titles
from faker import Faker
from faker.providers import DynamicProvider
from datetime import datetime, timedelta
from project.sessionmaker import Session as session_maker
import os
from dotenv import load_dotenv
load_dotenv()

UPLOAD_URL = os.getenv("UPLOAD_URL")

fake = Faker()

course_title_provider = DynamicProvider( # Custom course titles.
    provider_name="course_titles",
    elements=course_titles,
)
fake.add_provider(course_title_provider)

def generate_course_name():
    return fake.course_titles()

def generate_random_uid(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def teacher_generator():
    return user_generator('TEACHER')
def student_generator():
    return user_generator('STUDENT')
def admin_generator():
    return user_generator('ADMIN')
def user_generator(role):
    user = User(uid=generate_random_uid(),
                            role=role,
                            display_name=fake.name())
    return user

def course_student_generator(course_id, uid):
    return CourseStudent(course_id=course_id, uid=uid)
def course_admin_generator(course_id, uid):
    return CourseAdmin(course_id=course_id, uid=uid)


def run_seeder(uid):
    into_the_db(uid)

def generate_course(teacher_uid):
    course = Course(name=generate_course_name(),
                    teacher=teacher_uid)
    return course

def generate_projects(course_id, num_projects):
    projects = []
    for _ in range(num_projects):
        deadlines = []
        # Generate a random number of deadlines (1 to 3)
        num_deadlines = random.randint(1, 3)

        for _ in range(num_deadlines):
            future_datetime = datetime.now() + timedelta(days=random.randint(1, 30))
            deadline = (fake.catch_phrase(), future_datetime)
            deadlines.append(deadline)
        project = Project(course_id=course_id,
                          title=fake.catch_phrase(),
                          description=fake.catch_phrase(),
                          deadlines=deadlines,
                          visible_for_students=random.choice([True, False]),
                          archived=random.choice([True, False]),
                          regex_expressions=[]
                        )
        projects.append(project)
    return projects

def generate_submissions(project_id, student_uid):
    submissions = []
    num_submissions = random.randint(0, 2)
    for _ in range(num_submissions):
        submission = Submission(project_id=project_id,
                                uid=student_uid,
                                submission_time=datetime.now(),
                                submission_path="",
                                submission_status=random.choice([SubmissionStatus.SUCCESS, SubmissionStatus.FAIL, SubmissionStatus.LATE, SubmissionStatus.RUNNING]))
        graded = random.choice([True, False])
        if graded and submission.submission_status == "SUCCESS":
            submission.grading = random.randint(0, 20)
        submissions.append(submission)
    return submissions

def into_the_db(my_uid):
    try:
        session = session_maker()
        students = []
        num_students = random.randint(100, 200) #make a random amount of 100-200 students which we can use later to populate courses
        for _ in range(num_students):
            student = student_generator()
            students.append(student) # make the students
            session.add(student)
            session.commit()

        teachers = [] # same as students but for teachers
        num_teachers = random.randint(5, 10) 
        for _ in range(num_teachers):
            teacher = teacher_generator()
            teachers.append(teacher)
            session.add(teacher)
            session.commit() #only after commit uid becomes available 

        for _ in range(5):
            course = generate_course(my_uid) #make some courses where we are teacher
            session.add(course)
            session.commit()
            course_id = course.course_id
            teacher_relation = course_admin_generator(course_id, my_uid)
            session.add(teacher_relation)
            session.commit()

            # Add students to the course
            num_students_in_course = random.randint(5, 30)
            subscribed_students = []
            selected_students = set()
            while len(subscribed_students) < num_students_in_course:
                student = random.choice(students)
                if student.uid not in selected_students:
                    student_relation = course_student_generator(course_id, student.uid)
                    session.add(student_relation)
                    session.commit()
                    subscribed_students.append(student)
                    selected_students.add(student.uid)

            projects = generate_projects(course_id, 2)
            for project in projects:
                session.add(project)
                session.commit()
                print(project)
                project_id = project.project_id

                # Write assignment.md file
                assignment_content = fake.text()
                assignment_file_path = os.path.join(UPLOAD_URL,"projects", str(project_id), "assignment.md")
                os.makedirs(os.path.dirname(assignment_file_path), exist_ok=True)
                with open(assignment_file_path, "w") as assignment_file:
                    assignment_file.write(assignment_content)

                # Make submissions, 0 1 or 2 for each project per student 
                for student in subscribed_students:
                    submissions = generate_submissions(project_id, student.uid)
                    for submission in submissions:
                        session.add(submission)
                        session.commit()
                        submission_directory = os.path.join(UPLOAD_URL, "projects", str(project_id), "submissions", str(submission.submission_id), "submission")
                        os.makedirs(submission_directory, exist_ok=True)
                        submission_file_path = os.path.join(submission_directory, "submission.md") #TODO: seed a proper code submission?
                        with open(submission_file_path, "w") as submission_file:
                            submission_file.write(fake.text())

                        submission.submission_path = submission_directory
                        session.commit() # update submission path
                
    finally:
        # Rollback
        session.rollback()
        session.close()