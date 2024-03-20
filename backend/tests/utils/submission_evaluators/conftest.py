"""
This file contains the global fixtures for the submission evaluators tests.
"""
from shutil import rmtree
from os import environ, mkdir, path
import pytest
from project.models.submission import Submission
from project.models.project import Project

@pytest.fixture
def submission_root():
    """
    Create a submission root folder for the tests.
    When the tests are done, the folder is removed recursively.
    """
    submission_root = path.join(path.dirname(__file__), "submissions-root")
    environ["SUBMISSIONS_ROOT_PATH"] = submission_root
    mkdir(submission_root)
    yield submission_root
    rmtree(submission_root)

def prep_submission(submission_root: str) -> tuple[Submission, Project]:
    """
    Prepare a submission for testing by creating the appropriate files and 
    submission and project model objects.

    Args:
        submission_root (str): The folder of the submission to prepare.

    Returns:
        tuple: The submission and project model objects.
    """
    project_id = 2
    submission = Submission(submission_id=2, project_id=project_id)
    root = path.join(path.dirname(__file__), "resources", submission_root)
    submission.submission_path = path.join(root, "submission")
    project = Project(project_id=project_id, test_path=path.join(root, "assignment"))
    if not path.exists(path.join(submission.submission_path, "output")):
        mkdir(path.join(submission.submission_path, "output"))
    return submission, project

def cleanup_after_test(submission_root: str) -> None:
    """
    Remove the submission output root folder after a test.
    """
    rmtree(path.join(submission_root, "output"))
