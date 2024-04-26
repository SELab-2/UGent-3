from project.models.user import User
from project.models.course import Course
from project.db_in import db
import random
import string
from .elements import course_titles
from faker import Faker
from faker.providers import DynamicProvider

fake = Faker()

course_title_provider = DynamicProvider(
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
                            display_name=fake.name()),
    return user

def test_generator():
    teacher = teacher_generator()
    student = student_generator()
    admin = admin_generator()
    print(generate_course())
    print(admin)
    print(teacher)
    print(student)

def generate_course(teacher_uid=None):
    teacher = teacher_uid 
    if teacher == None:
        temp = teacher_generator()
        print(temp)
        teacher = temp[0].uid

    course = Course(name=generate_course_name(),
                    teacher=teacher)
    return course