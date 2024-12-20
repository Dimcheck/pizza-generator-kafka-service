#!/bin/bash

ENV_FILE="./src/pizza_service/configs/.env"

# Check if the .env file exists
if [ ! -f "$ENV_FILE" ]; then
  echo "Error: .env file not found!"
  exit 1
fi

# Load the environment variables from the .env file
# This assumes the .env file contains lines like: VAR=value
export $(grep -v '^#' "$ENV_FILE" | xargs)


gnome-terminal -- bash -c "cd src/pizza_service; \
    docker run --name my-mysql-container \
        -e MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD \
        -e MYSQL_DATABASE=$MYSQL_DATABASE \
        -e MYSQL_USER=$MYSQL_USER \
        -e MYSQL_PASSWORD=$MYSQL_PASSWORD \
        -p 3307:3306 \
        -d mysql/mysql-server:latest"


gnome-terminal -- bash -c "docker compose up -d"