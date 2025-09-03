.PHONY: help run migrate makemigrations superuser seed lint test \
        docker-build docker-up docker-down docker-logs collectstatic

help:
	@echo "Доступные команды:"
	@echo "  run             — запустить dev-сервер (0.0.0.0:8000)"
	@echo "  makemigrations  — создать миграции"
	@echo "  migrate         — применить миграции"
	@echo "  superuser       — создать суперпользователя"
	@echo "  seed            — загрузить тестовые данные"
	@echo "  lint            — проверка стиля (flake8)"
	@echo "  test            — тесты (pytest)"
	@echo "  collectstatic   — собрать статику"
	@echo "  docker-build    — пересобрать контейнер (без кеша)"
	@echo "  docker-up       — поднять контейнеры (build + up)"
	@echo "  docker-down     — остановить контейнеры"
	@echo "  docker-logs     — посмотреть логи контейнера web"

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
