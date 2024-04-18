"""
This module contains the endpoint for downloading a submission.
"""

import zipfile
import io
from os import getenv, path, walk
from urllib.parse import urljoin
from flask import Response, stream_with_context
from flask_restful import Resource
from project.models.submission import Submission

API_HOST = getenv("API_HOST")
UPLOAD_FOLDER = getenv("UPLOAD_FOLDER")
BASE_URL = urljoin(f"{API_HOST}/", "/submissions")

class SubmissionDownload(Resource):
    """
    Resource to download a submission.
    """
    def get(self, submission_id: int):
        """
        Download a submission as a zip file.
        """
        submission = Submission.query.get(submission_id)
        if submission is None:
            return {
                "message": f"Submission (submission_id={submission_id}) not found",
                "url": BASE_URL}, 404

        submission_path = path.join(
            UPLOAD_FOLDER,
            str(submission.project_id),
            "submissions",
            str(submission_id))
        print(submission_path)
        if not path.exists(submission_path) or not path.isdir(submission_path):
            return {"message": "Submission directory not found", "url": BASE_URL}, 404

        def zip_directory_stream():
            with io.BytesIO() as memory_file:
                with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:

                    for dirname, _, files in walk(submission_path):
                        zf.write(dirname, path.relpath(dirname, start=submission_path))
                        for filename in files:
                            file_path = path.join(dirname, filename)
                            zf.write(file_path, path.relpath(file_path, start=submission_path))

                memory_file.seek(0)
                data = memory_file.read(4096)
                while data:
                    yield data
                    data = memory_file.read(4096)

        response = Response(stream_with_context(zip_directory_stream()), mimetype='application/zip')
        response.headers['Content-Disposition'] = \
            f'attachment; filename="submission_{submission_id}.zip"'
        return response
