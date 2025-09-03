# Quotes App (Django)

Django-приложение для работы с цитатами:
- на главной странице показывается случайная цитата (с учётом веса);
- можно добавлять новые цитаты (без дублей, не более 3 на один источник);
- лайки, дизлайки и счётчик просмотров;
- страница топ-10 цитат по лайкам;
- админка Django;
- фикстуры для быстрого наполнения;
- CI (GitHub Actions) с flake8 и pytest;
- Docker для локального запуска.

---

## Локальный запуск (без Docker)
```bash
git clone
cd it-solution

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py loaddata quotes/fixtures/seed.json
python manage.py runserver 0.0.0.0:8000
```

Приложение будет доступно на http://127.0.0.1:8000

## Локальный запуск (Docker)
```bash
docker compose up --build
```
Приложение будет доступно на http://127.0.0.1:8000

## Тесты и линтер
```bash
flake8 .
pytest -q
```

## CI
В GitHub Actions настроен workflow:
- установка зависимостей,
- проверка кода flake8,
- прогон тестов pytest.

## Фикстуры
Быстрый импорт начальных данных:
```bash
python manage.py loaddata quotes/fixtures/seed.json
```

## Белан Вадим
Тестовое задание Python/Django.
