#!/bin/bash


tests_manifest_file="/tests/req-manifest.txt"

if [ -f "$tests_manifest_file" ]; then
    echo "Tests manifest file found. Installing tests requirements..."
    pip3 install -r $tests_manifest_file &> /dev/null
else
    echo "No tests manifest file found."
    submission_requirements_file="/submission/requirements.txt"
    if [ -f "$submission_requirements_file" ]; then
        echo "Requirements file found. Installing requirements..."
        pip3 install -r $submission_requirements_file &> /dev/null
    else
        echo "No requirements file found."
    fi

    submission_dev_requirements_file="/submission/dev-requirements.txt"

    if [ -f "$submission_dev_requirements_file" ]; then
        echo "Dev requirements file found. Installing dev requirements..."
        pip3 install -r $submission_dev_requirements_file &> /dev/null
    else
        echo "No dev requirements file found."
    fi

    tests_requirements_file="/tests/requirements.txt"

    if [ -f "$tests_requirements_file" ]; then
        echo "Tests requirements file found. Installing tests requirements..."
        pip3 install -r $tests_requirements_file &> /dev/null
    else
        echo "No tests requirements file found."
    fi
fi

echo "Running tests..."
ls /submission
bash /tests/run_tests.sh