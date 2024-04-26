from .elements import course_titles
from faker import Faker
from faker.providers import DynamicProvider

fake = Faker()

course_title_provider = DynamicProvider(
    provider_name="course_titles",
    elements=course_titles,
)

fake.add_provider(course_title_provider)
