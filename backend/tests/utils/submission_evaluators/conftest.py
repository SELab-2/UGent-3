import pytest
from shutil import rmtree
from os import environ, mkdir, path

@pytest.fixture
def submission_root():
    submission_root = path.join(path.dirname(__file__), "submissions-root")
    environ["SUBMISSIONS_ROOT_PATH"] = submission_root
    mkdir(submission_root)
    yield submission_root
    rmtree(submission_root)