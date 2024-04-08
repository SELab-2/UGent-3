"""
This file contains tests for the python submission evaluator.
"""

from os import path, listdir
import pytest
from project.utils.submissions.evaluator import evaluate
from project.utils.submissions.file_handling import create_submission_folder
from project.models.submission import Submission
from project.models.project import Project
from .conftest import prep_submission, cleanup_after_test

@pytest.fixture
def project_path_succes():
    """
    Return the path to a project with a succesful test case.
    """
    return path.join(path.dirname(__file__), "resources", "python", "tc_1/assignment")

@pytest.fixture
def evaluate_python(submission_root, project_path_succes):
    """Evaluate a python submission with a succesful test case."""
    project_id = 1
    submission = Submission(submission_id=1, project_id=project_id)
    submission.submission_path = create_submission_folder(submission_root, project_id)
    return evaluate(submission, project_path_succes, "python"), submission.submission_path

def prep_submission_and_clear_after_py(tc_folder: str) -> tuple[Submission, Project]:
    """
    Prepare a submission for testing by creating the appropriate files and
    submission and project model objects.

    Args:
        tc_folder (str): The folder of the test case to prepare.
    
    Returns:
        tuple: The submission and project model objects.
    """
    return prep_submission(path.join("python", tc_folder))

def test_base_python_evaluator(evaluate_python):
    """Test whether the base python evaluator works."""
    exit_code, _ = evaluate_python
    assert exit_code == 0

def test_makes_output_folder(evaluate_python):
    """Test whether the evaluator makes the output folder."""
    _, submission_path = evaluate_python
    assert path.exists(path.join(submission_path, "output"))

def test_makes_log_file(evaluate_python):
    """Test whether the evaluator makes the log file."""
    _, submission_path = evaluate_python
    assert path.exists(path.join(submission_path, "output", "test_output.log"))

def test_logs_output(evaluate_python):
    """Test whether the evaluator logs the output of the script."""
    _, submission_path = evaluate_python
    with open(path.join(submission_path, "output", "test_output.log",),
              "r", 
              encoding="utf-8") as output_file:
        assert "Hello, World!" in output_file.read()

def test_with_dependency():
    """Test whether the evaluator works with a dependency."""
    submission, project = prep_submission_and_clear_after_py("tc_2")
    exit_code = evaluate(submission, project, "python")
    cleanup_after_test(submission.submission_path)
    assert exit_code == 0

def test_dependency_manifest():
    """Test whether the evaluator works with a dependency manifest."""
    submission, project = prep_submission_and_clear_after_py("tc_3")
    exit_code = evaluate(submission, project, "python")
    cleanup_after_test(submission.submission_path)
    assert exit_code != 0
