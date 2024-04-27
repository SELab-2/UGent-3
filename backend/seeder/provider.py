from faker.providers import DynamicProvider
from seeder import fake
from elements import course_titles

course_title_provider = DynamicProvider(
     provider_name="course_titles",
     elements=course_titles,
)

fake.add_provider(course_title_provider)