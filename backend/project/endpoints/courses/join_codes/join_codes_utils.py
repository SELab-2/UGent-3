
from project.endpoints.courses.courses_utils import get_course_abort_if_not_found

def check_course_exists(func):
    """
    Middleware to check if the course exists before handling the request
    """
    def wrapper(self, course_id, join_code, *args, **kwargs):
        get_course_abort_if_not_found(course_id)
        return func(self, course_id, join_code, *args, **kwargs)
    return wrapper