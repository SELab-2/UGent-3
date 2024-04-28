#!/bin/bash

# Run Docker Compose to build and start the services, and capture the exit code from the test runner service
docker compose -f tests.yaml up --build --exit-code-from test-runner

# Store the exit code in a variable
exit_code=$?

# After the tests are finished, stop and remove the containers
docker compose -f tests.yaml down

# Check the exit code to determine whether the tests passed or failed
if [ $exit_code -eq 0 ]; then
    echo "Tests passed!"
else
    echo "Tests failed!"
fi

# Exit with the same exit code as the test runner service
exit $exit_code
