# lectureLib MVP

Простое Django-приложение для демонстрации библиотеки видеолекций.

## Что внутри

- каталог курсов;
- страница курса со списком видео;
- страница просмотра с Bunny embed player;
- Django admin для добавления курсов и видео;
- SQLite по умолчанию;
- автоматическая поддержка Postgres через `DATABASE_URL`;
- static files через WhiteNoise;
- запуск через `gunicorn` для Railway/Replit.

## Локальный запуск

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Откройте `http://127.0.0.1:8000/`, а данные добавляйте через `/admin/`.

## Railway

1. Создайте новый проект из GitHub-репозитория.
2. Добавьте переменные:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `DJANGO_ALLOWED_HOSTS=.up.railway.app,.railway.app`
   - `CSRF_TRUSTED_ORIGINS=https://*.up.railway.app,https://*.railway.app`
   - `DJANGO_SUPERUSER_USERNAME`
   - `DJANGO_SUPERUSER_PASSWORD`
   - `DJANGO_SUPERUSER_EMAIL`
3. Если нужен Postgres, добавьте Railway Postgres. Приложение понимает и `DATABASE_URL`, и Railway-переменные `PGDATABASE`, `PGUSER`, `PGPASSWORD`, `PGHOST`, `PGPORT`.
4. Railway запустит `sh bin/start` из `railway.json`.
5. В логах должна появиться строка `Starting gunicorn on 0.0.0.0:8000`. Target port в Networking должен совпадать с этим портом.

## Replit

1. Импортируйте репозиторий в Replit.
2. Установите зависимости из `requirements.txt`.
3. В Secrets добавьте:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `DJANGO_ALLOWED_HOSTS=.replit.app,.replit.dev,.repl.co`
   - `CSRF_TRUSTED_ORIGINS=https://*.replit.app,https://*.replit.dev,https://*.repl.co`
4. Запускайте:

```bash
python manage.py migrate --noinput
python manage.py collectstatic --noinput
gunicorn projectConfig.wsgi:application --bind 0.0.0.0:$PORT
```

Видео не проксируются через Django: в админке хранится Bunny embed URL, а браузер пользователя загружает плеер напрямую с Bunny.
