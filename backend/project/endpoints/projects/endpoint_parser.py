"""
Parser for the argument when posting or patching a project
"""

from flask_restful import reqparse
import werkzeug

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, help='Projects title', location="form")
parser.add_argument('descriptions', type=str, help='Projects description', location="form")
parser.add_argument('assignment_file', type=werkzeug.datastructures.FileStorage, help='Projects assignment file', location="form")
parser.add_argument("deadline", type=str, help='Projects deadline', location="form")
parser.add_argument("course_id", type=str, help='Projects course_id', location="form")
parser.add_argument("visible_for_students", type=bool, help='Projects visibility for students', location="form")
parser.add_argument("archieved", type=bool, help='Projects', location="form")
parser.add_argument("test_path", type=str, help='Projects test path', location="form")
parser.add_argument("script_name", type=str, help='Projects test script path', location="form")
parser.add_argument("regex_expressions", type=str, help='Projects regex expressions', location="form")


def parse_project_params():
    """
    Return a dict of every non None value in the param
    """
    args = parser.parse_args()
    result_dict = {}
    print(args)

    for key, value in args.items():
        if value is not None:
            result_dict[key] = value

    return result_dict
