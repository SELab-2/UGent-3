"""
Module that implements the /projects endpoint of the API
"""
import os
from urllib.parse import urljoin
import zipfile
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

from flask import request, jsonify
from flask_restful import Resource

from project.db_in import db
from project.utils.authentication import authorize_teacher

from project.endpoints.projects.endpoint_parser import parse_project_params

API_URL = os.getenv('API_HOST')
UPLOAD_FOLDER = os.getenv('UPLOAD_URL')


class ProjectsEndpoint(Resource):
    """
    Class for projects endpoints
    Inherits from flask_restful.Resource class
    for implementing get method
    """

    @authorize_teacher
    def get(self, teacher_id=None):
        """
        Get method for listing all available projects
        that are currently in the API
        """
        response_url = urljoin(API_URL, "projects")

        try:
            custom_sql_query = '''
                SELECT 
                    jsonb_build_object(
                        'project_id', project_id, 
                        'title', title, 
                        'description', description,
                        'deadlines', ARRAY_AGG(
                                        jsonb_build_object(
                                            'deadline_description', d.deadline_description, 
                                            'deadline', to_char(d.deadline, 'YYYY-MM-DD HH24:MI:SS TZ')
                                        ) 
                                    )
                    ) AS result_tuple
                FROM 
                    projects p
                JOIN 
                    unnest(p.deadlines) AS d(deadline_description, deadline) ON true
                GROUP BY 
                    project_id, title, description;
            '''
            projects = db.session.execute(text(custom_sql_query))
            projects_array = []
            # disables because pylinter says it's not iterable while the alchemySQL type is iterable
            for project in projects: # pylint: disable=E1133
                projects_array.append(project[0])

            respone = {
                "data": projects_array,
                "messsage": "Recources fetched succesfully",
                "url": response_url
            }
            return jsonify(respone), 200

        except SQLAlchemyError:
            return {"error": "Something went wrong while querying the database.",
                    "url": API_URL}, 500

    @authorize_teacher
    def post(self, teacher_id=None):
        """
        Post functionality for project
        using flask_restfull parse lib
        """
        file = request.files["assignment_file"]

        project_json = parse_project_params()
        filename = None

        if "assignment_file" in request.files:
            file = request.files["assignment_file"]
            filename = os.path.basename(file.filename)

        try:
            sql_insert = f'''
            INSERT 
            INTO projects 
            (title, description, deadlines, course_id, visible_for_students, archived, regex_expressions)
            VALUES ('{project_json["title"]}', '{project_json["description"]}', ARRAY['''

            # Add deadlines
            for deadline in project_json["deadlines"]:
                sql_insert += f'''ROW('{deadline["description"]}', '{deadline["deadline"]}')'''
                if deadline != project_json["deadlines"][-1]:
                    sql_insert += ','

            sql_insert += f'''
                ]::deadline[],
                {project_json["course_id"]}, {project_json["visible_for_students"]},
                 {project_json["archived"]}, ARRAY['''

            # Add regex expressions
            for regex in project_json["regex_expressions"]:
                sql_insert += f'''\'{regex}\''''
                if regex != project_json["regex_expressions"][-1]:
                    sql_insert += ','

            sql_insert += ''']) RETURNING ROW_TO_JSON(projects.*) AS insterted_data;'''

            sql_statement = text(sql_insert)
            query_result = db.session.execute(sql_statement)
            db.session.commit()
            new_project = query_result.fetchone()[0]
        except SQLAlchemyError:
            db.session.rollback()
            return (jsonify({
                "message": "Something went wrong in the database",
                "url": f"{API_URL}/projects",}), 500)

        project_upload_directory = os.path.join(f"{UPLOAD_FOLDER}", f"{new_project['project_id']}")
        os.makedirs(project_upload_directory, exist_ok=True)
        if filename is not None:
            try:
                file_path = os.path.join(project_upload_directory, filename)
                file.save(file_path)
                with zipfile.ZipFile(file_path) as upload_zip:
                    upload_zip.extractall(project_upload_directory)
            except zipfile.BadZipfile:
                os.remove(os.path.join(project_upload_directory, filename))
                db.session.rollback()
                return ({
                            "message": "Please provide a .zip file for uploading the instructions",
                            "url": f"{API_URL}/projects"
                        },
                        400)
        return {
            "message": "Project created succesfully",
            "data": new_project,
            "url": f"{API_URL}/projects/{new_project['project_id']}"
        }, 201
