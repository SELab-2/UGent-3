"""
This module contains functions for handling files and folders for submissions.
"""

from os import path, makedirs, getenv

def create_submission_subfolders(submission_path: str):
    """
    Create the output and artifacts folder for a submission.
    """
    submission_output_path = path.join(submission_path, "output")
    artifacts_path = path.join(submission_output_path, "artifacts")
    submission_solution_path = path.join(submission_path, "submission")

    if not path.exists(submission_solution_path):
        makedirs(submission_solution_path)
    
    if not path.exists(submission_output_path):
        makedirs(submission_output_path)

    if not path.exists(artifacts_path):
        makedirs(artifacts_path)

    return submission_output_path

def create_submission_folder(submission_id: int, project_id: int):
    """
    Create the submission folder and the submission
    solution folder that will contain a students solution.

    Args:
        submission_id (int): The id of the submission.
        project_id (int): The id of the project.

    Returns:
        str: The path to the submission folder.
    """
    submission_path = path.join(getenv("SUBMISSIONS_ROOT_PATH"),
                                str(project_id),
                                str(submission_id))

    if not path.exists(submission_path):
        makedirs(submission_path)

    create_submission_subfolders(submission_path)

    return submission_path
