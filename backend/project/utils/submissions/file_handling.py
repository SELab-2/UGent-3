from os import path, makedirs, getenv

def create_submission_subfolders(submission_path: str):
    submission_output_path = path.join(submission_path, "output")
    artifacts_path = path.join(submission_output_path, "artifacts")

    if not path.exists(submission_output_path):
        makedirs(submission_output_path)

    if not path.exists(artifacts_path):
        makedirs(artifacts_path)

    return submission_output_path

def create_submission_folder(submission_id, project_id):
    submission_path = path.join(getenv("SUBMISSIONS_ROOT_PATH"), str(project_id), str(submission_id))
    submission_solution_path = path.join(submission_path, "submission")

    if not path.exists(submission_path):
        makedirs(submission_path)

    if not path.exists(submission_solution_path):
        makedirs(submission_solution_path)

    return submission_path