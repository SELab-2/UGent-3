#!/bin/sh
# Start the Docker daemon in the background
dockerd-entrypoint.sh &

# Wait for the Docker daemon to start
until docker info; do
    echo "Waiting for Docker daemon to start..."
    sleep 1
done

# Execute the command passed to the docker run command
exec "$@"
