#!/bin/bash

# Check if a port number was provided as an argument
if [ -z "$1" ]; then
  echo "Usage: $0 <port>"
  exit 1
fi

PORT=$1

# Check if the port is a valid number
if ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
  echo "Error: Port must be a number."
  exit 1
fi

# Construct the docker run command with the provided port
DOCKER_CMD="sudo docker run -p ${PORT}:8080 hapiproject/hapi:latest"

# Open a new terminal and run the Docker command
# This example uses gnome-terminal. You might need to change this depending on your terminal emulator.
gnome-terminal -- bash -c "$DOCKER_CMD; exec bash"
