# Python evaluator
## General usage
This evaluator is responsible for running and executing tests on a student's Python code.

## Structure
When submitting the project a teacher can add a requirements manifest `req-manifest.txt`, this way only the packages in the requirements file are usable on the evaluator.

When no manifest is present, students are able to install their own depedencies with a `requirements.txt` and a `dev-requirements.txt`.
Or the teacher can add a `requirements.txt` if they want to pre install dependencies that a are present for testing the project.

## Running tests
When a `run_tests.sh` is present in the project assignment files, it will be run when the student is submitting their code.
When running tests, it's important to note that the root of the student's submission will be `/submission`.
