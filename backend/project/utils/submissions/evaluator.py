from project.models.projects import Projects
from os import path, makedirs
from os import getenv
from project.models.submissions import Submissions
import docker

DOCKER_IMAGE_MAPPER = {
    "python": path.join(path.dirname(__file__), "evaluators", "python"),
}

def evaluate(submission: Submissions, project: Projects, evaluator: str):
    project_path = project.test_path

    docker_image = DOCKER_IMAGE_MAPPER.get(evaluator, None)
    if docker_image is None:
        docker_image = project_path
        if not path.exists(docker_image):
            raise Exception(f"Test path: {docker_image}, not found")
    
    submission_path = submission.submission_path
    submission_solution_path = path.join(submission_path, "submission")

    container = create_and_run_evaluator(docker_image, submission.submission_id, project_path, submission_solution_path)

    submission_output_path = create_submission_subfolders(submission_path)
    test_output_path = path.join(submission_output_path, "test_output.log")

    exit_code = container.wait()

    with open(path.join(test_output_path, ), "w") as output_file:
        output_file.write(container.logs().decode('utf-8'))

    container.remove()

    return exit_code['StatusCode']

def create_and_run_evaluator(docker_image: str, submission_id: int, project_path: str, submission_solution_path: str):
    client = docker.from_env()
    image, build_logs = client.images.build(path=docker_image, tag=f"submission_{submission_id}")
      
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
