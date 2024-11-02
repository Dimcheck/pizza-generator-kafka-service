#!/bin/bash
gnome-terminal -- bash -c "echo 'This is Kafka Service!'; docker compose up; read -p 'Press Enter to stop...'"
gnome-terminal -- bash -c "echo 'This is Pizza Generator!';       cd src/pizza_service;   poetry install; poetry run uvicorn app:app --host 0.0.0.0 --port 8000 --reload; read -p 'Press Enter to stop...'"
gnome-terminal -- bash -c "echo 'This is Sauce Service !';        cd src/sauce_service;   poetry install; poetry run python main.py; read -p 'Press Enter to stop...'"
gnome-terminal -- bash -c "echo 'This is Cheese Service !';       cd src/cheese_service;  poetry install; poetry run python main.py; read -p 'Press Enter to stop...'"
gnome-terminal -- bash -c "echo 'This is Meat Service !';         cd src/meat_service;    poetry install; poetry run python main.py; read -p 'Press Enter to stop...'"
gnome-terminal -- bash -c "echo 'This is Vegies Service !';       cd src/veggie_service;  poetry install; poetry run python main.py; read -p 'Press Enter to stop...'"
gnome-terminal -- bash -c "echo 'This is Movie Tickets Service!'; cd src/movie_service;   poetry install; poetry run python main.py; read -p 'Press Enter to stop...'"