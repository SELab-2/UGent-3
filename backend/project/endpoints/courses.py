"""Courses api point"""
from flask import Blueprint, jsonify, request
from flask import abort
from flask_restful import Api, Resource
from project.models.course_relations import CourseAdmins, CourseStudents
from project.models.users import Users
from project.models.courses import Courses
from project.models.projects import Projects
from project import db
from sqlalchemy.exc import SQLAlchemyError

courses_bp = Blueprint("courses", __name__)
courses_api = Api(courses_bp)


def execute_query_abort_if_db_error(query, all=False):
    """
    Execute a SQLAlchemy query and handle any SQLAlchemyError that might occur.
    If all == True, the query will be executed with the all() method, otherwise with the first() method.
    Args:
        query (Query): The SQLAlchemy query to execute.

    Returns:
        ResultProxy: The result of the query if successful, otherwise aborts with error 500.
    """
    try:
        if all:
            result = query.all()
        else:
            result = query.first()
    except SQLAlchemyError as e:
        abort(500, str(e))
    return result

def add_or_delete_abort_if_error(to_add_or_delete, delete=False):
    """
    Add a new object to the database and handle any SQLAlchemyError that might occur.

    Args:
        to_add (object): The object to add to the database.
    """
    try:
        if delete:
            db.session.delete(to_add_or_delete)
        else:
            db.session.add(to_add_or_delete)
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(500, str(e))

def commit_abort_if_error():
    """
    Commit the current session and handle any SQLAlchemyError that might occur.
    """
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(500, str(e))

def abort_if_not_teacher_or_none_assistant(course_id, teacher, assistant):
    """
    Check if the current user is authorized to appoint new admins to a course.

    Args:
        course_id (int): The ID of the course.

    Raises:
        HTTPException: If the current user is not authorized or if the UID of the person to be made an admin is missing in the request body.
    """
    abort_if_uid_is_none(teacher)

    course = get_course_abort_if_not_found(course_id)

    if teacher != course.teacher:
        abort(
            403,
            "Only teachers can appoint new admins to a course",
        )

    if not assistant:
        abort(400, "uid of person to make admin is required in the request body")

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
    get_course_abort_if_not_found(course_id)
    abort_if_no_user_found_for_uid(uid)

    query = CourseAdmins.query.filter_by(uid=uid, course_id=course_id)
    admin_relation = execute_query_abort_if_db_error(query)
    if not admin_relation:
        abort(
            403,
            """Not authorized to assign new students to a course, 
            you should be an admin for this course""",
        )

    if not student_uids:
        abort(
            400,
            """To assign new students to a course,
            you should have a students field with a list of uids in the request body""",
        )

def abort_if_uid_is_none(uid):
    """
    Check wether the uid is None if so
    abort with error 400
    """
    if uid is None:
        abort(400, "There should be an uid in the request query")

def abort_if_no_user_found_for_uid(uid):
    """
    Check if a user exists based on the provided uid.

    Args:
        uid (int): The unique identifier of the user.

    Raises:
        NotFound: If the user with the given uid is not found.
    """
    query = Users.query.filter_by(uid=uid)
    user = execute_query_abort_if_db_error(query)

    if not user:
        abort(404, "User was not found")
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
        CourseAdmins.query.filter_by(uid=uid, course_id=course_id)
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
    course = execute_query_abort_if_db_error(query)

    if not course:
        return json_message("Course not found"), 404

    return course


class CoursesForUser(Resource):
    """Api endpoint for the /courses link"""

    def post(self):
        """
        This function will create a new course
        if the body of the post contains a name and uid is an admin or teacher
        """
        uid = request.args.get("uid")
        abort_if_uid_is_none(uid)

        user = abort_if_no_user_found_for_uid(uid)

        if not user.is_teacher:
            message = "Only teachers or admins can create new courses, you are unauthorized"
            return json_message(message), 403

        data = request.get_json()

        if "name" not in data:
            message = "Missing 'name' in the request body"
            return json_message(message), 400

        name = data["name"]
        new_course = Courses(name=name, teacher=uid)
        if "ufora_id" in data:
            new_course.ufora_id = data["ufora_id"]

        add_or_delete_abort_if_error(new_course)
        commit_abort_if_error()

        admin_course = CourseAdmins(uid=uid, course_id=new_course.course_id)
        add_or_delete_abort_if_error(admin_course)
        commit_abort_if_error()

        message = (
            "Course with name:"
            + name
            + "and course_id:"
            + new_course.course_id
            + " was succesfully created"
        )
        return json_message(message), 201


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
                where projects are jsons containing the title,deadline and project_id
            ]
        }
        """
        uid = request.args.get("uid")
        abort_if_uid_is_none(uid)
        admin = get_admin_relation(uid, course_id)
        query = CourseStudents.query.filter_by(uid=uid, course_id=course_id)
        student = execute_query_abort_if_db_error(query)

        if not (admin or student):
            message = "User is nor an admin, nor a student of this course"
            return json_message(message), 404

        course = get_course_abort_if_not_found(course_id)
        query = Projects.query.filter_by(course_id=course_id, all=True)
        project_uids = [
            project.project_id
            for project in execute_query_abort_if_db_error(query, all=True)
        ]
        query = CourseAdmins.query.filter_by(course_id=course_id)
        admin_uids = [
            admin.uid for admin in execute_query_abort_if_db_error(query, all=True)
        ]
        query = CourseStudents.query.filter_by(course_id=course_id)
        student_uids = [
            student.uid for student in execute_query_abort_if_db_error(query, all=True)
        ]

        data = {
            "ufora_id": course.ufora_id,
            "teacher": course.teacher,
            "admins": admin_uids,
            "students": student_uids,
            "projects": project_uids,
        }

        return jsonify(data)

    def delete(self, course_id):
        """
        This function will delete the course with course_id
        """
        uid = request.args.get("uid")
        abort_if_uid_is_none(uid)

        admin = get_admin_relation(uid, course_id)

        if not admin:
            message = "You are not an admin of this course and so you cannot delete it"
            return json_message(message), 403

        course = get_course_abort_if_not_found(course_id)
        add_or_delete_abort_if_error(course, delete=True)
        commit_abort_if_error()

        response = {
            "message": "Succesfully deleted course with course_id: " + str(course_id)
        }
        return jsonify(response)


class CoursesForAdmins(Resource):
    """
    This class will handle post and delete queries to
    the /courses/course_id/admins url, only the teacher of a course can do this
    """

    def get(self, course_id):
        """
        This function will return all the admins of a course
        """
        get_course_abort_if_not_found(course_id)

        query = CourseAdmins.query.filter_by(course_id=course_id)
        admin_uids = [a.uid for a in execute_query_abort_if_db_error(query, all=True)]
        return jsonify(admin_uids)

    def post(self, course_id):
        """
        Api endpoint for adding new admins to a course, can only be done by the teacher
        """
        teacher = request.args.get("uid")
        data = request.get_json()
        assistant = data.get("admin_uid")
        abort_if_not_teacher_or_none_assistant(course_id, teacher, assistant)

        query = Users.query.filter_by(uid=assistant)
        new_admin = execute_query_abort_if_db_error(query)
        if not new_admin:
            message = "User to make admin was not found, please request with a valid uid"
            return json_message(message), 404

        admin_relation = CourseAdmins(uid=assistant, course_id=course_id)
        add_or_delete_abort_if_error(admin_relation)
        commit_abort_if_error()

        return json_message(
            "Admin " + assistant + " added to course " + str(course_id)
        ), 201

    def delete(self, course_id):
        """
        Api endpoint for removing admins of a course, can only be done by the teacher
        """
        teacher = request.args.get("uid")
        data = request.get_json()
        assistant = data.get("admin_uid")
        abort_if_not_teacher_or_none_assistant(course_id, teacher, assistant)

        query = CourseAdmins.query.filter_by(uid=assistant, course_id=course_id)
        admin_relation = execute_query_abort_if_db_error(query)
        if not admin_relation:
            message = "Course with given admin not found"
            return json_message(message), 404

        add_or_delete_abort_if_error(admin_relation, delete=True)
        commit_abort_if_error()

        message = "Admin " + assistant + " was succesfully removed from course " + str(course_id)
        return json_message(message), 204


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

        get_course_abort_if_not_found(course_id)

        query = CourseStudents.query.filter_by(course_id=course_id)
        student_uids = [s.uid for s in execute_query_abort_if_db_error(query, all=True)]

        return jsonify(student_uids)

    def post(self, course_id):
        """
        Allows admins of a course to assign new students by posting to:
        /courses/course_id/students with a list of uid in the request body under key "students"
        """
        uid = request.args.get("uid")
        data = request.get_json()
        student_uids = data.get("students")
        abort_if_none_uid_student_uids_or_non_existant_course_id(
            course_id, uid, student_uids
        )

        for uid in student_uids:
            query = CourseStudents.query.filter_by(uid=uid, course_id=course_id)
            student_relation = execute_query_abort_if_db_error(query)
            if student_relation:
                db.session.rollback()
                message = "Student with uid " + uid + " is already assigned to the course"
                return json_message(message), 400
            add_or_delete_abort_if_error(CourseStudents(uid=uid, course_id=course_id))
        commit_abort_if_error()

        return json_message("Users were succesfully added to the course"), 201

    def delete(self, course_id):
        """
        This function allows admins of a course to remove students by sending a delete request to
        /courses/course_id/students with inside the request body
        a field "students" = [list of uids to unassign]
        """
        uid = request.args.get("uid")
        data = request.get_json()
        student_uids = data.get("students")
        abort_if_none_uid_student_uids_or_non_existant_course_id(
            course_id, uid, student_uids
        )

        for uid in student_uids:
            query = CourseStudents.query.filter_by(uid=uid, course_id=course_id)
            student_relation = execute_query_abort_if_db_error(query)
            if student_relation:
                add_or_delete_abort_if_error(student_relation, delete=True)
        commit_abort_if_error()

        response = {"message": "Users were succesfully removed from the course"}
        return jsonify(response)


courses_api.add_resource(CoursesForUser, "/courses")

courses_api.add_resource(CoursesByCourseId, "/courses/<int:course_id>")

courses_api.add_resource(CoursesForAdmins, "/courses/<int:course_id>/admins")

courses_api.add_resource(CoursesToAddStudents, "/courses/<int:course_id>/students")
