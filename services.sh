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


gnome-terminal -- bash -c "echo 'This is DB Service!'; cd src/pizza_service; \
    docker run --name my-mysql-container \
        -e MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD \
        -e MYSQL_DATABASE=$MYSQL_DATABASE \
        -e MYSQL_USER=$MYSQL_USER \
        -e MYSQL_PASSWORD=$MYSQL_PASSWORD \
        -p 3307:3306 \
        -d mysql/mysql-server:latest"


gnome-terminal -- bash -c "echo 'This is Kafka Service!'; docker compose up; read -p 'Press Enter to stop...'"
gnome-terminal -- bash -c "echo 'This is Pizza Generator!';       cd src/pizza_service;   poetry install; poetry run alembic upgrade head; poetry run uvicorn app:app --host 0.0.0.0 --port 8000 --reload; read -p 'Press Enter to stop...'"
gnome-terminal -- bash -c "echo 'This is Sauce Service !';        cd src/sauce_service;   poetry install; poetry run python main.py; read -p 'Press Enter to stop...'"
gnome-terminal -- bash -c "echo 'This is Cheese Service !';       cd src/cheese_service;  poetry install; poetry run python main.py; read -p 'Press Enter to stop...'"
gnome-terminal -- bash -c "echo 'This is Meat Service !';         cd src/meat_service;    poetry install; poetry run python main.py; read -p 'Press Enter to stop...'"
gnome-terminal -- bash -c "echo 'This is Vegies Service !';       cd src/veggie_service;  poetry install; poetry run python main.py; read -p 'Press Enter to stop...'"
gnome-terminal -- bash -c "echo 'This is Movie Tickets Service!'; cd src/movie_service;   poetry install; poetry run python main.py; read -p 'Press Enter to stop...'"