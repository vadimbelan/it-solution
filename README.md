## Быстрый старт (локально)
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations quotes
python manage.py migrate
python manage.py runserver
