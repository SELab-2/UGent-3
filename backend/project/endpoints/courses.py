"""Courses api point"""
from flask import Blueprint, jsonify, request
from flask import abort
from flask_restful import Api, Resource
from project.models.course_relations import CourseAdmins, CourseStudents
from project.models.users import Users
from project.models.courses import Courses
from project.models.projects import Projects
from project import db

courses_bp = Blueprint("courses", __name__)
courses_api = Api(courses_bp)
# TODO: functions to allow teachers to add students to a course


def check_uid():
    """
    Check wether the request query contained a uid if yes return it,
    otherwise abort with error 400
    """
    uid = request.args.get("uid")
    if uid is None:
        abort(400, "There should be a uid in the request query")
    return uid


class CoursesForUser(Resource):
    """Api endpoint for the /courses link"""

    def get(self):
        """
        Get function for /courses
        returns all the courses of a related users in a json structure,
        with courses represented as {course_id:...,name:...}
        {
            student: [list of courses where user is registered as student]
            admin: [list of courses where user is registered as admin]
        }
        """
        uid = check_uid()

        user = Users.query.filter_by(uid=uid).first()

        if not user:
            abort(404, "User was not found")

        student_course_ids = [
            course_relation.course_id
            for course_relation in CourseStudents.query.filter_by(uid=uid).all()
        ]
        admin_course_ids = [
            course_relation.course_id
            for course_relation in CourseAdmins.query.filter_by(uid=uid).all()
        ]

        student_course_data = Courses.query.filter(
            Courses.course_id.in_(student_course_ids)
        ).all()
        admin_course_data = Courses.query.filter(
            Courses.course_id.in_(admin_course_ids)
        ).all()

        courses_data = {
            "student": [
                {"course_id": course.course_id, "name": course.name}
                for course in student_course_data
            ],
            "admin": [
                {"course_id": course.course_id, "name": course.name}
                for course in admin_course_data
            ],
        }

        return jsonify(courses_data)

    def post(self):
        """
        This function will create a new course
        if the body of the post contains a name and uid is an admin or teacher
        """
        uid = check_uid()

        user = Users.query.filter_by(uid=uid).first()

        if not user:
            abort(404, "User with given uid not found")

        if not (user.is_teacher or user.is_admin):
            abort(
                403,
                "Only teachers or admins can create new courses, you are unauthorized",
            )

        data = request.get_json()

        if "name" not in data:
            abort(400, "Missing 'name' in the request body")

        name = data["name"]
        new_course = Courses(name=name, teacher=uid)
        if "ufora_id" in data:
            new_course.ufora_id = data["ufora_id"]

        db.session.add(new_course)
        db.session.commit()

        admin_course = CourseAdmins(uid=uid, course_id=new_course.course_id)
        db.session.add(admin_course)
        db.session.commit()


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
        uid = check_uid()
        is_admin = (
            CourseAdmins.query.filter_by(uid=uid, course_id=course_id).first()
            is not None
        )
        is_student = (
            CourseStudents.query.filter_by(uid=uid, course_id=course_id).first()
            is not None
        )

        if not (is_admin or is_student):
            abort(404, "User is not related to this course")

        course = Courses.query.filter_by(course_id=course_id).first()

        if not course:
            abort(404, "Course was not found")

        projects = Projects.query.filter_by(course_id=course_id).all()

        projects_json = [
            {
                "project_id": project.project_id,
                "title": project.title,
                "deadline": project.deadline,
            }
            for project in projects
        ]

        data = {
            "course": {"name": course.name, "course_id": course.course_id},
            "projects": projects_json,
        }

        return jsonify(data)

    def delete(self, course_id):
        """
        This function will delete the course with course_id
        """
        uid = check_uid()

        admin = CourseAdmins.query.filter_by(uid=uid, course_id=course_id).first()

        if not admin:
            abort(
                403, "You are not an admin of this course and so you cannot delete it"
            )

        course = Courses.query.filter_by(course_id=course_id).first()
        if not course:
            abort(404, "Course not found")
        try:
            db.session.delete(course)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            abort(500, "Internal server error")
        response = {
            "Message": "Succesfully deleted course with course_id: " + str(course_id)
        }
        return jsonify(response)

class CoursesForAdmins(Resource):
    """
    This class will handle post and delete queries to
    the /courses/course_id/admins url, only the teacher of a course can do this
    """

    def post(self, course_id):
        """
        Api endpoint for adding new admins to a course, can only be done by the teacher
        """
        uid = check_uid()

        course = Courses.query.filter_by(course_id=course_id).first()
        
        if not course:
            abort(404, "Course not found")

        if uid != course.teacher:
            abort(
                403,
                "Only teachers can appoint new admins to a course",
            )

        data = request.get_json()
        admin_uid = data.get('admin_uid')
        if not admin_uid:
            abort(400, "uid of person to make admin is required in the request body")

        new_admin = Users.query.filter_by(uid=admin_uid).first()
        if not new_admin:
            abort(
                404, "User to make admin was not found, please request with a valid uid"
            )

        admin_relation = CourseAdmins(uid=admin_uid, course_id=course_id)
        db.session.add(admin_relation)
        db.session.commit()

        return jsonify(
            {"Message": "Admin " + admin_uid + " added to course " + str(course_id)}
        )

    def delete(self, course_id):
        """
        Api endpoint for removing admins of a course, can only be done by the teacher
        """
        uid = check_uid()

        course = Courses.query.filter_by(course_id=course_id).first()

        if not course:
            abort(404, "Course not found")

        if uid != course.teacher:
            abort(
                403,
                "Only teachers can remove admins from a course",
            )

        data = request.get_json()
        admin_uid = data.get("admin_uid")
        if not admin_uid:
            abort(
                400,
                "uid of person to remove from admins is required in the request body",
            )

        admin_relation = CourseAdmins.query.filter_by(
            uid=admin_uid, course_id=course_id
        ).first()
        if not admin_relation:
            abort(404, "There was no admin relation between the given uid and course")

        db.session.delete(admin_relation)
        db.session.commit()

        return jsonify({"Message": "Admin " + admin_uid + " removed from course " + str(course_id)})


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

        course = Courses.query.filter_by(course_id=course_id).first()

        if not course:
            abort(404, "Course not found")

        student_uids = [
            s.uid for s in CourseStudents.query.filter_by(course_id=course_id).all()
        ]
        
        response_data = {
            "students": student_uids
        }
        return jsonify(response_data)

    def post(self, course_id):
        """
        Allows admins of a course to assign new students by posting to:
        /courses/course_id/students with a list of uid in the request body under key "students"
        """
        course = Courses.query.filter_by(course_id=course_id).first()
        if not course:
            abort(404, "Course not found")

        uid = check_uid()
        user = Users.query.filter_by(uid=uid).first()
        if not user:
            abort(404, "User not found")

        admin_relation = CourseAdmins.query.filter_by(
            uid=uid, course_id=course_id
        ).first()
        if not admin_relation:
            abort(
                403,
                """Not authorized to assign new students to a course, 
                you should be an admin for this course""",
            )

        data = request.get_json()
        student_uids = data.get("students")
        if not student_uids:
            abort(
                400,
                """To assign new students to a course,
                you should have a students field with a list of uids in the request body""",
            )

        for uid in student_uids:
            student = Users.query.filter_by(uid=uid).first()
            if not student:
                db.session.rollback()
                abort(400, "Student with uid " + uid + " does not exist")
            student_relation = CourseStudents.query.filter_by(
                uid=uid, course_id=course_id
            ).first()
            if student_relation:
                db.session.rollback()
                abort(400, "Student with uid " + uid + " is already assigned to the course")
            db.session.add(CourseStudents(uid=uid, course_id=course_id))
        db.session.commit()

        response = {"Message": "Users were succesfully assigned to the course"}
        return jsonify(response)

    def delete(self, course_id):
        """
        This function allows admins of a course to remove students by sending a delete request to
        /courses/course_id/students with inside the request body 
        a field "students" = [list of uids to unassign]
        """
        course = Courses.query.filter_by(course_id=course_id).first()
        if not course:
            abort(404, "Course not found")

        uid = check_uid()
        user = Users.query.filter_by(uid=uid).first()
        if not user:
            abort(404, "User not found")

        admin_relation = CourseAdmins.query.filter_by(
            uid=uid, course_id=course_id
        ).first()
        if not admin_relation:
            abort(
                403,
                """Not authorized to remove students from a course,
                  you should be an admin for this course""",
            )

        data = request.get_json()
        student_uids = data.get("students")
        if not student_uids:
            abort(
                400,
                """To assign new students to a course 
                you should have a students field with a list of uids in the request body""",
            )

        db.session.query(CourseStudents).filter(
            CourseStudents.course_id == course_id, CourseStudents.uid.in_(student_uids)
        ).delete(
            synchronize_session=False
        )
        db.session.commit()

        response = {"Message": "Users were succesfully removed from the course"}
        return jsonify(response)


courses_api.add_resource(CoursesForUser, "/courses")

courses_api.add_resource(CoursesByCourseId, "/courses/<int:course_id>")

courses_api.add_resource(CoursesForAdmins, "/courses/<int:course_id>/admins")

courses_api.add_resource(CoursesToAddStudents, "/courses/<int:course_id>/students")
