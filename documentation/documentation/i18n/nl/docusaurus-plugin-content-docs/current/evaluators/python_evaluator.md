# Python evaluator
## General usage
This evaluator is responsible for running and executing tests on a student's Python code.

## Structure
When submitting the project a teacher can add a requirments manifest `filename of manifest`, this way only the packages in the requirments file are installable on the evaluator.

When no manifest is present students are able to install their own depedencies with a `requirments.txt` and a `dev-requirments.txt`.

## Running tests
When a `run_tests.sh` is present in the project assignment files, it will be run when the student is submitting his code.
