"""
Parser for the argument when posting or patching a project
"""

from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, help='Projects title')
parser.add_argument('descriptions', type=str, help='Projects description')
parser.add_argument('assignment_file', type=str, help='Projects assignment file')
parser.add_argument("deadline", type=str, help='Projects deadline')
parser.add_argument("course_id", type=str, help='Projects course_id')
parser.add_argument("visible_for_students", type=bool, help='Projects visibility for students')
parser.add_argument("archived", type=bool, help='Projects')
parser.add_argument("test_path", type=str, help='Projects test path')
parser.add_argument("script_name", type=str, help='Projects test script path')
parser.add_argument("regex_expressions", type=str, help='Projects regex expressions')


def parse_project_params():
    """
    Return a dict of every non None value in the param
    """
    args = parser.parse_args()
    result_dict = {}

    for key, value in args.items():
        if value is not None:
            result_dict[key] = value

    return result_dict
