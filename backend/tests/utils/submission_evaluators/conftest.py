"""
This file contains the global fixtures for the submission evaluators tests.
"""
from shutil import rmtree
from os import environ, mkdir, path
import pytest
from project.models.submissions import Submissions
from project.models.projects import Projects

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

def prep_submission(submission_root: str) -> tuple[Submissions, Projects]:
    """
    Prepare a submission for testing by creating the appropriate files and 
    submission and project model objects.

    Args:
        submission_root (str): The folder of the submission to prepare.

    Returns:
        tuple: The submission and project model objects.
    """
    project_id = 2
    submission = Submissions(submission_id=2, project_id=project_id)
    root = path.join(path.dirname(__file__), "resources", submission_root)
    submission.submission_path = path.join(root, "submission")
    project = Projects(project_id=project_id, test_path=path.join(root, "assignment"))
    mkdir(path.join(submission.submission_path, "output"))
    return submission, project

def cleanup_after_test(submission_root: str) -> None:
    """
    Remove the submission output root folder after a test.
    """
    rmtree(path.join(submission_root, "output"))
