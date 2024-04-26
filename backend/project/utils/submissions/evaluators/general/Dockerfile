# Use Ubuntu as the base image
FROM ubuntu:latest

# Avoiding user interaction with tzdata, etc.
ENV DEBIAN_FRONTEND=noninteractive

# Update and install basic dependencies
RUN apt-get update && apt-get install -y \
    software-properties-common \
    build-essential \
    curl \
    wget \
    git \
    cmake  # Adding CMake for C/C++ project management

# Install Python
RUN apt-get install -y python3 python3-pip

# Install Node.js
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get install -y nodejs

# Install Java
RUN apt-get install -y openjdk-11-jdk

# Install Ruby
RUN apt-get install -y ruby-full

# Clean up to reduce the image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .