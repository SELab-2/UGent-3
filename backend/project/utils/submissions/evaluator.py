"""
This module is responsible for evaluating the submission.
It uses docker to run the evaluator in a container.
The image used for the container is determined by the evaluator argument.
If the evaluator is not found in the
DOCKER_IMAGE_MAPPER, the project test path is used as the image.
The evaluator is run in the container and the
exit code is returned. The output of the evaluator is written to a log file
in the submission output folder.
"""
from os import path, makedirs
import docker
from sqlalchemy.exc import SQLAlchemyError
from project.db_in import db
from project.models.submission import Submission


EVALUATORS_FOLDER = path.join(path.dirname(__file__), "evaluators")

DOCKER_IMAGE_MAPPER = {
    "PYTHON": path.join(EVALUATORS_FOLDER, "python"),
    "GENERAL": path.join(EVALUATORS_FOLDER, "general")
}


def evaluate(submission: Submission, project_path: str, evaluator: str, is_late: bool) -> int:
    """
    Evaluate a submission using the evaluator.

    Args:
        submission (Submissions): The submission to evaluate.
        project_path (str): The path to the project.
        evaluator (str): The evaluator to use.
    
    Returns:
        int: The exit code of the evaluator.
    
    Raises:
        ValueError: If the evaluator is not found in the DOCKER_IMAGE_MAPPER
                    and the project test path does not exist.
    """

    docker_image = DOCKER_IMAGE_MAPPER.get(evaluator, None)
    if docker_image is None:
        docker_image = project_path
        if not path.exists(docker_image):
            raise ValueError(f"Test path: {docker_image},\
                             not found and the provided evaluator:\
                             {evaluator} is not associated with any image.")

    submission_path = submission.submission_path
    submission_solution_path = path.join(submission_path, "submission")

    container = create_and_run_evaluator(docker_image,
                                         submission.submission_id,
                                         project_path,
                                         submission_solution_path)

    submission_output_path = path.join(submission_path, "output")
    makedirs(submission_output_path, exist_ok=True)
    test_output_path = path.join(submission_output_path, "test_output.log")

    exit_code = container.wait()

    with open(path.join(test_output_path), "w", encoding='utf-8') as output_file:
        output_file.write(container.logs().decode('utf-8'))

    container.remove()

    return exit_code['StatusCode']

def run_evaluator(submission: Submission, project_path: str, evaluator: str, is_late: bool) -> int:
    """
    Run the evaluator for the submission.

    Args:
        submission (Submission): The submission to evaluate.
        project_path (str): The path to the project.
        evaluator (str): The evaluator to use.
        is_late (bool): Whether the submission is late.

    Returns:
        int: The exit code of the evaluator.
    """
    status_code = evaluate(submission, project_path, evaluator, is_late)

    if not is_late:
        if status_code == 0:
            submission.submission_status = 'SUCCESS'
        else:
            submission.submission_status = 'FAIL'
    else:
        submission.submission_status = 'LATE'

    try:
        db.session.merge(submission)
        db.session.commit()
    except SQLAlchemyError:
        pass

    return status_code


def create_and_run_evaluator(docker_image: str,
                             submission_id: int,
                             project_path: str,
                             submission_solution_path: str):
    """
    Create and run the evaluator container.

    Args:
        docker_image (str): The path to the docker image.
        submission_id (int): The id of the submission.
        project_path (str): The path to the project.
        submission_solution_path (str): The path to the submission solution.

    Returns:
        docker.models.containers.Container: The container that is running the evaluator.
    """
    client = docker.from_env()
    image, _ = client.images.build(path=docker_image, tag=f"submission_{submission_id}")


    container = client.containers.run(
        image.id,
        detach=True,
        command="bash entry_point.sh",
        volumes={
            path.abspath(project_path): {'bind': "/tests", 'mode': 'rw'},
            path.abspath(submission_solution_path): {'bind': "/submission", 'mode': 'rw'}
        },
        stderr=True,
        stdout=True,
        pids_limit=256
    )
    return container
