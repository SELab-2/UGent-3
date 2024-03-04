"""Courses api point"""

from os import getenv
from dotenv import load_dotenv
from flask import Blueprint, jsonify, request
from flask import abort
from flask_restful import Api, Resource
from sqlalchemy.exc import SQLAlchemyError
from project.models.course_relations import CourseAdmins, CourseStudents
from project.models.users import Users
from project.models.courses import Courses
from project.models.projects import Projects
from project import db

courses_bp = Blueprint("courses", __name__)
courses_api = Api(courses_bp)

load_dotenv()
API_URL = getenv("API_HOST")


def execute_query_abort_if_db_error(query, url, query_all=False):
    """
    Execute the given SQLAlchemy query and handle any SQLAlchemyError that might occur.
    If query_all == True, the query will be executed with the all() method,
    otherwise with the first() method.
    Args:
        query (Query): The SQLAlchemy query to execute.

    Returns:
        ResultProxy: The result of the query if successful, otherwise aborts with error 500.
    """
    try:
        if query_all:
            result = query.all()
        else:
            result = query.first()
    except SQLAlchemyError as e:
        response = json_message(str(e))
        response["url"] = url
        abort(500, description=response)
    return result


def add_abort_if_error(to_add, url):
    """
    Add a new object to the database
    and handle any SQLAlchemyError that might occur.

    Args:
        to_add (object): The object to add to the database.
    """
    try:
        db.session.add(to_add)
    except SQLAlchemyError as e:
        db.session.rollback()
        response = json_message(str(e))
        response["url"] = url
        abort(500, description=response)


def delete_abort_if_error(to_delete, url):
    """
    Deletes the given object from the database
    and aborts the request with a 500 error if a SQLAlchemyError occurs.

    Args:
    - to_delete: The object to be deleted from the database.
    """
    try:
        db.session.delete(to_delete)
    except SQLAlchemyError as e:
        db.session.rollback()
        response = json_message(str(e))
        response["url"] = url
        abort(500, description=response)


def commit_abort_if_error(url):
    """
    Commit the current session and handle any SQLAlchemyError that might occur.
    """
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        response = json_message(str(e))
        response["url"] = url
        abort(500, description=response)


def abort_if_not_teacher_or_none_assistant(course_id, teacher, assistant):
    """
    Check if the current user is authorized to appoint new admins to a course.

    Args:
        course_id (int): The ID of the course.

    Raises:
        HTTPException: If the current user is not authorized or
        if the UID of the person to be made an admin is missing in the request body.
    """
    url = API_URL + "/courses/" + str(course_id) + "/admins"
    abort_if_uid_is_none(teacher, url)

    course = get_course_abort_if_not_found(course_id)

    if teacher != course.teacher:
        response = json_message("Only the teacher of a course can appoint new admins")
        response["url"] = url
        abort(403, description=response)

    if not assistant:
        response = json_message(
            "uid of person to make admin is required in the request body"
        )
        response["url"] = url
        abort(400, description=response)


def abort_if_none_uid_student_uids_or_non_existant_course_id(
    course_id, uid, student_uids
):
    """
    Check the request to assign new students to a course.

    Args:
        course_id (int): The ID of the course.

    Raises:
        403: If the user is not authorized to assign new students to the course.
        400: If the request body does not contain the required 'students' field.
    """
    url = API_URL + "/courses/" + str(course_id) + "/students"
    get_course_abort_if_not_found(course_id)
    abort_if_no_user_found_for_uid(uid, url)
    query = CourseAdmins.query.filter_by(uid=uid, course_id=course_id)
    admin_relation = execute_query_abort_if_db_error(query, url)
    if not admin_relation:
        message = "Not authorized to assign new students to course with id " + str(
            course_id
        )
        response = json_message(message)
        response["url"] = url
        abort(403, description=response)

    if not student_uids:
        message = """To assign new students to a course,
                     you should have a students field with a list of uids in the request body"""
        response = json_message(message)
        response["url"] = url
        abort(400, description=response)


def abort_if_uid_is_none(uid, url):
    """
    Check whether the uid is None if so
    abort with error 400
    """
    if uid is None:
        response = json_message("There should be a uid in the request query")
        response["url"] = url
        abort(400, description=response)


def abort_if_no_user_found_for_uid(uid, url):
    """
    Check if a user exists based on the provided uid.

    Args:
        uid (int): The unique identifier of the user.

    Raises:
        NotFound: If the user with the given uid is not found.
    """
    query = Users.query.filter_by(uid=uid)
    user = execute_query_abort_if_db_error(query, url)

    if not user:
        response = json_message("User with uid " + uid + " was not found")
        response["url"] = url
        abort(404, description=response)
    return user


def get_admin_relation(uid, course_id):
    """
    Retrieve the CourseAdmins object for the given uid and course.

    Args:
        uid (int): The user ID.
        course_id (int): The course ID.

    Returns:
        CourseAdmins: The CourseAdmins object if the user is an admin, otherwise None.
    """
    return execute_query_abort_if_db_error(
        CourseAdmins.query.filter_by(uid=uid, course_id=course_id),
        url=API_URL + "/courses/" + str(course_id) + "/admins",
    )


def json_message(message):
    """
    Create a json message with the given message.

    Args:
        message (str): The message to include in the json.

    Returns:
        dict: The message in a json format.
    """
    return {"message": message}


def get_course_abort_if_not_found(course_id):
    """
    Get a course by its ID.

    Args:
        course_id (int): The course ID.

    Returns:
        Courses: The course with the given ID.
    """
    query = Courses.query.filter_by(course_id=course_id)
    course = execute_query_abort_if_db_error(query, API_URL + "/courses")

    if not course:
        response = json_message("Course not found")
        response["url"] = API_URL + "/courses"
        abort(404, description=response)

    return course


class CoursesForUser(Resource):
    """Api endpoint for the /courses link"""

    def get(self):
        """ "
        Get function for /courses this will be the main endpoint
        to get all courses and filter by given query parameter like /courses?parameter=...
        parameters can be either one of the following: teacher,ufora_id,name.
        """
        query = Courses.query
        if "teacher" in request.args:
            query = query.filter_by(course_id=request.args.get("teacher"))
        if "ufora_id" in request.args:
            query = query.filter_by(ufora_id=request.args.get("ufora_id"))
        if "name" in request.args:
            query = query.filter_by(name=request.args.get("name"))
        results = execute_query_abort_if_db_error(
            query, url=API_URL + "/courses", query_all=True
        )
        detail_urls = [
            f"{API_URL}/courses/{str(course.course_id)}" for course in results
        ]
        message = "Succesfully retrieved all courses with given parameters"
        response = json_message(message)
        response["data"] = detail_urls
        response["url"] = API_URL + "/courses"
        return response

    def post(self):
        """
        This function will create a new course
        if the body of the post contains a name and uid is an admin or teacher
        """
        abort_url = API_URL + "/courses"
        uid = request.args.get("uid")
        abort_if_uid_is_none(uid, abort_url)

        user = abort_if_no_user_found_for_uid(uid, abort_url)

        if not user.is_teacher:
            message = (
                "Only teachers or admins can create new courses, you are unauthorized"
            )
            return json_message(message), 403

        data = request.get_json()

        if "name" not in data:
            message = "Missing 'name' in the request body"
            return json_message(message), 400

        name = data["name"]
        new_course = Courses(name=name, teacher=uid)
        if "ufora_id" in data:
            new_course.ufora_id = data["ufora_id"]

        add_abort_if_error(new_course, abort_url)
        commit_abort_if_error(abort_url)

        admin_course = CourseAdmins(uid=uid, course_id=new_course.course_id)
        add_abort_if_error(admin_course, abort_url)
        commit_abort_if_error(abort_url)

        message = (f"Course with name: {name} and"
                   f"course_id:{new_course.course_id} was succesfully created")
        response = json_message(message)
        data = {
            "course_id": API_URL + "/courses/" + str(new_course.course_id),
            "name": new_course.name,
            "teacher": API_URL + "/users/" + new_course.teacher,
            "ufora_id": new_course.ufora_id if new_course.ufora_id else "None",
        }
        response["data"] = data
        response["url"] = API_URL + "/courses/" + str(new_course.course_id)
        return response, 201


class CoursesByCourseId(Resource):
    """Api endpoint for the /courses/course_id link"""

    def get(self, course_id):
        """
        This get function will return all the related projects of the course
        in the following form:
        {
            course: course with course_id
            projects: [
                list of all projects that have course_id
                where projects are jsons containing the title, deadline and project_id
            ]
        }
        """
        abort_url = API_URL + "/courses"
        uid = request.args.get("uid")
        abort_if_uid_is_none(uid, abort_url)
        admin = get_admin_relation(uid, course_id)
        query = CourseStudents.query.filter_by(uid=uid, course_id=course_id)
        student = execute_query_abort_if_db_error(query, abort_url)

        if not (admin or student):
            message = "User is not an admin, nor a student of this course"
            return json_message(message), 404

        course = get_course_abort_if_not_found(course_id)
        query = Projects.query.filter_by(course_id=course_id)
        abort_url = API_URL + "/courses/" + str(course_id)
        # course does exist so url should be to the id
        project_uids = [
            API_URL + "/projects/" + project.project_id
            for project in execute_query_abort_if_db_error(
                query, abort_url, query_all=True
            )
        ]
        query = CourseAdmins.query.filter_by(course_id=course_id)
        admin_uids = [
            API_URL + "/users/" + admin.uid
            for admin in execute_query_abort_if_db_error(
                query, abort_url, query_all=True
            )
        ]
        query = CourseStudents.query.filter_by(course_id=course_id)
        student_uids = [
            API_URL + "/users/" + student.uid
            for student in execute_query_abort_if_db_error(
                query, abort_url, query_all=True
            )
        ]

        data = {
            "ufora_id": course.ufora_id,
            "teacher": API_URL + "/users/" + course.teacher,
            "admins": admin_uids,
            "students": student_uids,
            "projects": project_uids,
        }
        response = json_message(
            "Succesfully retrieved course with course_id: " + str(course_id)
        )
        response["data"] = data
        response["url"] = API_URL + "/courses/" + str(course_id)
        return response

    def delete(self, course_id):
        """
        This function will delete the course with course_id
        """
        abort_url = API_URL + "/courses/"
        uid = request.args.get("uid")
        abort_if_uid_is_none(uid, abort_url)

        admin = get_admin_relation(uid, course_id)

        if not admin:
            message = "You are not an admin of this course and so you cannot delete it"
            return json_message(message), 403

        course = get_course_abort_if_not_found(course_id)
        abort_url = API_URL + "/courses/" + str(course_id)
        # course does exist so url should be to the id
        delete_abort_if_error(course, abort_url)
        commit_abort_if_error(abort_url)

        response = {
            "message": "Succesfully deleted course with course_id: " + str(course_id),
            "url": API_URL + "/courses",
        }
        return response

    def patch(self, course_id):
        """
        This function will update the course with course_id
        """
        abort_url = API_URL + "/courses/"
        uid = request.args.get("uid")
        abort_if_uid_is_none(uid, abort_url)

        admin = get_admin_relation(uid, course_id)

        if not admin:
            message = "You are not an admin of this course and so you cannot update it"
            return json_message(message), 403

        data = request.get_json()
        course = get_course_abort_if_not_found(course_id)
        abort_url = API_URL + "/courses/" + str(course_id)
        if "name" in data:
            course.name = data["name"]
        if "teacher" in data:
            course.teacher = data["teacher"]
        if "ufora_id" in data:
            course.ufora_id = data["ufora_id"]

        commit_abort_if_error(abort_url)
        response = json_message(
            "Succesfully updated course with course_id: " + str(course_id)
        )
        response["url"] = API_URL + "/courses/" + str(course_id)
        data = {
            "course_id": API_URL + "/courses/" + str(course.course_id),
            "name": course.name,
            "teacher": API_URL + "/users/" + course.teacher,
            "ufora_id": course.ufora_id if course.ufora_id else "None",
        }
        response["data"] = data
        return response, 200


class CoursesForAdmins(Resource):
    """
    This class will handle post and delete queries to
    the /courses/course_id/admins url, only the teacher of a course can do this
    """

    def get(self, course_id):
        """
        This function will return all the admins of a course
        """
        abort_url = API_URL + "/courses/" + str(course_id) + "/admins"
        get_course_abort_if_not_found(course_id)

        query = CourseAdmins.query.filter_by(course_id=course_id)
        admin_uids = [
            API_URL + "/users/" + a.uid
            for a in execute_query_abort_if_db_error(query, abort_url, query_all=True)
        ]
        response = json_message(
            "Succesfully retrieved all admins of course " + str(course_id)
        )
        response["data"] = admin_uids
        response["url"] = abort_url  # not actually aborting here tho heheh
        return jsonify(admin_uids)

    def post(self, course_id):
        """
        Api endpoint for adding new admins to a course, can only be done by the teacher
        """
        abort_url = API_URL + "/courses/" + str(course_id) + "/admins"
        teacher = request.args.get("uid")
        data = request.get_json()
        assistant = data.get("admin_uid")
        abort_if_not_teacher_or_none_assistant(course_id, teacher, assistant)

        query = Users.query.filter_by(uid=assistant)
        new_admin = execute_query_abort_if_db_error(query, abort_url)
        if not new_admin:
            message = (
                "User to make admin was not found, please request with a valid uid"
            )
            return json_message(message), 404

        admin_relation = CourseAdmins(uid=assistant, course_id=course_id)
        add_abort_if_error(admin_relation, abort_url)
        commit_abort_if_error(abort_url)
        response = json_message(
            f"Admin assistant added to course {course_id}"
        )
        response["url"] = abort_url
        data = {
            "course_id": API_URL + "/courses/" + str(course_id),
            "uid": API_URL + "/users/" + assistant,
        }
        response["data"] = data
        return response, 201

    def delete(self, course_id):
        """
        Api endpoint for removing admins of a course, can only be done by the teacher
        """
        abort_url = API_URL + "/courses/" + str(course_id) + "/admins"
        teacher = request.args.get("uid")
        data = request.get_json()
        assistant = data.get("admin_uid")
        abort_if_not_teacher_or_none_assistant(course_id, teacher, assistant)

        query = CourseAdmins.query.filter_by(uid=assistant, course_id=course_id)
        admin_relation = execute_query_abort_if_db_error(query, abort_url)
        if not admin_relation:
            message = "Course with given admin not found"
            return json_message(message), 404

        delete_abort_if_error(admin_relation, abort_url)
        commit_abort_if_error(abort_url)

        message = (
            f"Admin {assistant}"
            f" was succesfully removed from course {course_id}"
        )
        response = json_message(message)
        response["url"] = abort_url
        return response, 204


class CoursesToAddStudents(Resource):
    """
    Class that will respond to the /courses/course_id/students link
    teachers should be able to assign and remove students from courses,
    and everyone should be able to list all students assigned to a course
    """

    def get(self, course_id):
        """
        Get function at /courses/course_id/students
        to get all the users assigned to a course
        everyone can get this data so no need to have uid query in the link
        """
        abort_url = API_URL + "/courses/" + str(course_id) + "/students"
        get_course_abort_if_not_found(course_id)

        query = CourseStudents.query.filter_by(course_id=course_id)
        student_uids = [
            API_URL + "/users/" + s.uid
            for s in execute_query_abort_if_db_error(query, abort_url, query_all=True)
        ]
        response = json_message(
            "Succesfully retrieved all students of course " + str(course_id)
        )
        response["data"] = student_uids
        response["url"] = abort_url
        return response

    def post(self, course_id):
        """
        Allows admins of a course to assign new students by posting to:
        /courses/course_id/students with a list of uid in the request body under key "students"
        """
        abort_url = API_URL + "/courses/" + str(course_id) + "/students"
        uid = request.args.get("uid")
        data = request.get_json()
        student_uids = data.get("students")
        abort_if_none_uid_student_uids_or_non_existant_course_id(
            course_id, uid, student_uids
        )

        for uid in student_uids:
            query = CourseStudents.query.filter_by(uid=uid, course_id=course_id)
            student_relation = execute_query_abort_if_db_error(query, abort_url)
            if student_relation:
                db.session.rollback()
                message = (
                    "Student with uid " + uid + " is already assigned to the course"
                )
                return json_message(message), 400
            add_abort_if_error(CourseStudents(uid=uid, course_id=course_id), abort_url)
        commit_abort_if_error(abort_url)
        response = json_message("Users were succesfully added to the course")
        response["url"] = abort_url
        data = {"students": [API_URL + "/users/" + uid for uid in student_uids]}
        response["data"] = data
        return response, 201

    def delete(self, course_id):
        """
        This function allows admins of a course to remove students by sending a delete request to
        /courses/course_id/students with inside the request body
        a field "students" = [list of uids to unassign]
        """
        abort_url = API_URL + "/courses/" + str(course_id) + "/students"
        uid = request.args.get("uid")
        data = request.get_json()
        student_uids = data.get("students")
        abort_if_none_uid_student_uids_or_non_existant_course_id(
            course_id, uid, student_uids
        )

        for uid in student_uids:
            query = CourseStudents.query.filter_by(uid=uid, course_id=course_id)
            student_relation = execute_query_abort_if_db_error(query, abort_url)
            if student_relation:
                delete_abort_if_error(student_relation, abort_url)
        commit_abort_if_error(abort_url)

        response = json_message("Users were succesfully removed from the course")
        response["url"] = API_URL + "/courses/" + str(course_id) + "/students"
        return response


courses_api.add_resource(CoursesForUser, "/courses")

courses_api.add_resource(CoursesByCourseId, "/courses/<int:course_id>")

courses_api.add_resource(CoursesForAdmins, "/courses/<int:course_id>/admins")

courses_api.add_resource(CoursesToAddStudents, "/courses/<int:course_id>/students")
