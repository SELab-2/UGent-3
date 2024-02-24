"""
This file contains tests for the python submission evaluator.
"""

from project.utils.submissions.evaluator import evaluate, create_submission_folder
from project.models.submissions import Submissions
from project.models.projects import Projects
import pytest
from os import path

@pytest.fixture
def project_path_succes():
    return path.join(path.dirname(__file__), "resources", "python", "tc_1")

@pytest.fixture
def evaluate_python(submission_root, project_path_succes):
    """Evaluate a python submission with a succesful test case."""
    project_id = 1
    submission = Submissions(submission_id=1, project_id=project_id)
    submission.submission_path = create_submission_folder(submission_root, project_id)
    project = Projects(project_id=project_id, test_path=project_path_succes)
    return evaluate(submission, project, "python"), submission.submission_path

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
    with open(path.join(submission_path, "output", "test_output.log"), "r") as output_file:
        assert "Hello, World!" in output_file.read()
