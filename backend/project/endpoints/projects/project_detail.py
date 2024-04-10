"""
Module for project details page
for example /projects/1 if the project id of
the corresponding project is 1
"""
import os
import zipfile
from urllib.parse import urljoin
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import text

from flask import request, jsonify
from flask_restful import Resource

from project.db_in import db
from project.utils.authentication import authorize_teacher_or_project_admin, \
    authorize_teacher_of_project, authorize_project_visible

from project.endpoints.projects.endpoint_parser import parse_project_params

API_URL = os.getenv('API_HOST')
RESPONSE_URL = urljoin(API_URL, "projects")
UPLOAD_FOLDER = os.getenv('UPLOAD_URL')


class ProjectDetail(Resource):
    """
    Class for projects/id endpoints
    Inherits from flask_restful.Resource class
    for implementing get, delete and put methods
    """

    @authorize_project_visible
    def get(self, project_id):
        """
        Get method for listing a specific project
        filtered by id of that specific project
        the id fetched from the url with the reaparse
        """
        try:
            custom_sql_query = f'''
                SELECT 
                    ROW_TO_JSON(t) as json_data
                FROM (
                    SELECT
                        project_id, 
                        title, 
                        description, 
                        ARRAY_AGG(
                            jsonb_build_object(
                                'deadline_description', d.deadline_description, 
                                'deadline', to_char(d.deadline, 'YYYY-MM-DD HH24:MI:SS TZ')
                            ) 
                        ) AS deadlines,
                        p.course_id,
                        p.visible_for_students,
                        p.archived,
                        p.regex_expressions
                    FROM 
                        projects p,
                        unnest(p.deadlines) AS d(deadline_description, deadline)
                    WHERE 
                        p.project_id = {project_id}
                    GROUP BY 
                        project_id, 
                        title, 
                        description
                ) t;
            '''

            project = db.session.execute(text(custom_sql_query)).fetchone()

            if project:
                return {
                    "data": project[0],
                    "message": "Project fetched succesfully",
                    "url": f'{RESPONSE_URL}/{project_id}'
                }, 200
            return {
                "message": f"Project with {project_id} not found",
                "url": f'{RESPONSE_URL}'
            }, 404
        except SQLAlchemyError:
            db.session.rollback()
            return (jsonify({
                "error": "Something went wrong while querying the database",
                "url": f"{RESPONSE_URL}/{project_id}"
            }), 500)

    @authorize_teacher_or_project_admin
    def patch(self, project_id): # pylint: disable=R0914
        """
        Update method for updating a specific project
        filtered by id of that specific project
        """
        project_json = parse_project_params()

        try:
            patch_values = []
            for key, value in project_json.items():
                update = f"{key} = '{value}'"
                patch_values.append(update)

            sql_patch = f'''
            UPDATE projects SET {', '.join(patch_values)} 
            WHERE project_id = {project_id} 
            RETURNING ROW_TO_JSON(projects.*) AS updated_data;'''
            project = db.session.execute(text(sql_patch)).fetchone()
            if not project:
                return (jsonify({
                    "error": "Project was not found",
                    "url": RESPONSE_URL
                }), 404)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            return (jsonify({
                "error": "Something went wrong while updating the project",
                "url": RESPONSE_URL
            }, 500))

        if "assignment_file" in request.files:
            file = request.files["assignment_file"]
            filename = os.path.basename(file.filename)
            project_upload_directory = os.path.join(f"{UPLOAD_FOLDER}", f"{project_id}")
            os.makedirs(project_upload_directory, exist_ok=True)
            try:
                # remove the old file
                try:
                    to_rem_files = os.listdir(project_upload_directory)
                    for to_rem_file in to_rem_files:
                        to_rem_file_path = os.path.join(project_upload_directory, to_rem_file)
                        if os.path.isfile(to_rem_file_path):
                            os.remove(to_rem_file_path)
                except FileNotFoundError:
                    db.session.rollback()
                    return ({
                        "message": "Something went wrong deleting the old project files",
                        "url": f"{API_URL}/projects/{project_id}"
                    })

                # removed all files now upload the new files
                file.save(os.path.join(project_upload_directory, filename))
                zip_location = os.path.join(project_upload_directory, filename)
                with zipfile.ZipFile(zip_location) as upload_zip:
                    upload_zip.extractall(project_upload_directory)

            except zipfile.BadZipfile:
                db.session.rollback()
                return ({
                            "message":
                                "Please provide a valid .zip file for updating the instructions",
                            "url": f"{API_URL}/projects/{project_id}"
                        },
                        400)

        return (jsonify({
            "message": "Project patched succesfully",
            "data": project[0]
        }), 200)

    @authorize_teacher_of_project
    def delete(self, project_id):
        """
        Delete a project and all of its submissions in cascade
        done by project id
        """
        try:
            delete_query = f'''
                DELETE FROM projects WHERE project_id = {project_id} RETURNING project_id;
            '''
            deleted_project = db.session.execute(text(delete_query)).fetchone()
            if deleted_project is None:
                return (jsonify(
                    {"message": f"Project with {project_id} doesn't exist",
                     "url": RESPONSE_URL
                     }, 404))
            db.session.commit()
            return (jsonify({"message": "Resource deleted successfully",
                             "url": RESPONSE_URL}, 200))
        except SQLAlchemyError:
            db.session.rollback()
            return {"error": "Something went wrong deleting",
                    "url": RESPONSE_URL}, 500
