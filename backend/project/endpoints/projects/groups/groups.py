from os import getenv
from urllib.parse import urljoin
from dotenv import load_dotenv
from flask import request
from flask_restful import Resource

from project.models.group import Group
from project.utils.query_agent import query_selected_from_model, insert_into_model
from project.utils.authentication import login_required, authorize_teacher

load_dotenv()
API_URL = getenv("API_HOST")
RESPONSE_URL = urljoin(f"{API_URL}/", "groups")
class Groups(Resource):
    """Api endpoint for the /project/project_id/groups link"""

    @login_required
    def get(self, project_id):
        """
        Get function for /project/project_id/groups this will be the main endpoint
        to get all groups for a project
        """
        return query_selected_from_model(
            Group,
            RESPONSE_URL,
            url_mapper={"group_id": RESPONSE_URL},
            filters={"project_id": project_id}
        )

    @authorize_teacher
    def post(self, project_id, teacher_id=None):
        """
        This function will create a new group for a project
        if the body of the post contains a group_size and project_id exists
        """

        req = request.json
        req["project_id"] = project_id
        print(req)
        return insert_into_model(
            Group,
            req,
            RESPONSE_URL,
            "group_id",
            required_fields=["project_id", "size"]
        )
