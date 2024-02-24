from project.utils.submissions.file_handling import create_submission_folder
from os import path
from shutil import rmtree

def test_create_submission_folder_creates(submission_root):
    submission_id = 1
    project_id = 1
    submission_path = create_submission_folder(submission_id, project_id)
    assert path.join(submission_path) \
            == path.join(submission_root, str(project_id), str(submission_id))
    assert path.exists(submission_path)
    assert path.exists(path.join(submission_path, "submission"))
    rmtree(submission_path)