"""
Parser for the argument when posting or patching a project
"""

from flask_restful import reqparse
from werkzeug.datastructures import FileStorage
import json

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, help='Projects title', location="form")
parser.add_argument('description', type=str, help='Projects description', location="form")
parser.add_argument(
    'assignment_file',
    type=FileStorage,
    help='Projects assignment file',
    location="form"
)
parser.add_argument('deadlines', type=str, help='Projects deadlines', location="form")
parser.add_argument("course_id", type=str, help='Projects course_id', location="form")
parser.add_argument(
    "visible_for_students",
    type=bool,
    help='Projects visibility for students',
    location="form"
)
parser.add_argument("archived", type=bool, help='Projects', location="form")
parser.add_argument(
    "regex_expressions",
    type=str,
    help='Projects regex expressions',
    location="form"
)


def parse_project_params():
    """
    Return a dict of every non None value in the param
    """
    args = parser.parse_args()
    result_dict = {}
    for key, value in args.items():
        if value is not None:
            if "deadlines" == key:
                deadlines_parsed = json.loads(value)
                new_deadlines = []
                for deadline in deadlines_parsed:
                    new_deadlines.append(
                        (
                            deadline["description"],
                            deadline["deadline"]
                        )
                    )
                result_dict[key] = new_deadlines
            else:
                result_dict[key] = value

    return result_dict
