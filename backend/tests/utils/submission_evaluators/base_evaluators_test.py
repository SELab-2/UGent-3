"""
This file contains tests for functions that are applicable to all evaluators.
"""
from os import path
from shutil import rmtree
from project.utils.submissions.file_handling import create_submission_folder

def test_create_submission_folder_creates(submission_root):
    """
    Test whether the create_submission_folder function creates the submission folder.
    """
    submission_id = 1
    project_id = 1
    submission_path = create_submission_folder(submission_id, project_id)
    assert path.join(submission_path) \
            == path.join(submission_root, str(project_id), str(submission_id))
    assert path.exists(submission_path)
    assert path.exists(path.join(submission_path, "submission"))
    rmtree(submission_path)
