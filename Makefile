DOCKER_COMPOSE := docker compose
DOCKER_BACKEND_CMD := $(DOCKER_COMPOSE) exec web bash -c
BACKEND_SERVICE := web

docker-build:
	$(DOCKER_COMPOSE) up -d

docker-dev-all:
	$(DOCKER_COMPOSE) up

docker-dev-build:
	$(DOCKER_COMPOSE) up --build

pre-commit:
	pre-commit run --all-files

super-user:
	$(DOCKER_BACKEND_CMD) "python3 manage.py createsuperuser"

migrate:
	$(DOCKER_BACKEND_CMD) "python3 manage.py makemigrations && python3 manage.py migrate"

create-app:
	$(DOCKER_BACKEND_CMD) "cd apps && django-admin startapp $(appname)"

ruff:
	$(DOCKER_BACKEND_CMD) "ruff check"

ruff-format:
	$(DOCKER_BACKEND_CMD) "ruff format"

super-user:
	$(DOCKER_BACKEND_CMD) "python3 manage.py createsuperuser"