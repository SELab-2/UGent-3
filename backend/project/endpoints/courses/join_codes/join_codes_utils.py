"""
This module contains functions that are used by the join codes resources.
"""

from project.endpoints.courses.courses_utils import get_course_abort_if_not_found

def check_course_exists(func):
    """
    Middleware to check if the course exists before handling the request
    """
    def wrapper(*args, **kwargs):
        get_course_abort_if_not_found(kwargs["course_id"])
        return func(*args, **kwargs)
    return wrapper
