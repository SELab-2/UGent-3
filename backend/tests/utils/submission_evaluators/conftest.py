"""
This file contains the global fixtures for the submission evaluators tests.
"""
from shutil import rmtree
from os import environ, mkdir, path
import pytest

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
