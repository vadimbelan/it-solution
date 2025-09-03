.PHONY: help run migrate makemigrations superuser seed lint test \
        docker-build docker-up docker-down docker-logs collectstatic

help:
	@echo "Targets:"
	@echo "  run             - runserver 0.0.0.0:8000"
	@echo "  makemigrations  - make migrations"
	@echo "  migrate         - apply migrations"
	@echo "  superuser       - create superuser"
	@echo "  seed            - load seed fixtures"
	@echo "  lint            - flake8 ."
	@echo "  test            - pytest -q"
	@echo "  collectstatic   - manage.py collectstatic"
	@echo "  docker-build    - docker compose build --no-cache"
	@echo "  docker-up       - docker compose up --build"
	@echo "  docker-down     - docker compose down"
	@echo "  docker-logs     - docker compose logs -f web"

run:
	python manage.py runserver 0.0.0.0:8000

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

superuser:
	python manage.py createsuperuser

seed:
	python manage.py loaddata quotes/fixtures/seed.json

lint:
	flake8 .

test:
	pytest -q

collectstatic:
	python manage.py collectstatic --noinput

docker-build:
	docker compose build --no-cache

docker-up:
	docker compose up --build

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f web
