"""
This file is used to configure the join codes endpoints.
It is used to define the routes for the join codes blueprint and the
corresponding api endpoints.

The join codes blueprint is used to define the routes for the join codes api
endpoints and the join codes api is used to define the routes for the join codes
api endpoints.
"""

from flask import Blueprint
from flask_restful import Api

from project.endpoints.courses.join_codes.course_join_codes import CourseJoinCodes
from project.endpoints.courses.join_codes.course_join_code import CourseJoinCode

join_codes_bp = Blueprint("join_codes", __name__)
join_codes_api = Api(join_codes_bp)

join_codes_bp.add_url_rule("/courses/<int:course_id>/join_codes",
                           view_func=CourseJoinCodes.as_view('course_join_codes'))

join_codes_bp.add_url_rule("/courses/<int:course_id>/join_codes/<string:join_code>",
                            view_func=CourseJoinCode.as_view('course_join_code'))
