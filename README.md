# lectureLib MVP

Простое Django-приложение для демонстрации библиотеки видеолекций.

## Что внутри

- каталог курсов;
- главная страница-портал со списком курсов;
- `/courses/<id>/` сразу открывает страницу просмотра, имитируя ответ внешнего API;
- страница просмотра с Bunny embed player и метаданными из Bunny Stream API;
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
   - `BUNNY_STREAM_API_KEY` или `BUNNY_API_KEY`
   - `BUNNY_STREAM_EMBED_TOKEN_KEY`, только если в Bunny Stream включена защита Embed View Token Authentication
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

Видео не проксируются через Django: в админке хранится Bunny video ID, Django получает метаданные через Bunny Stream API, а браузер пользователя загружает плеер напрямую с Bunny.

## Bunny playback

`BUNNY_STREAM_API_KEY` используется только сервером Django для запроса метаданных видео. Если название и описание видео отображаются, этот ключ уже работает; полный API Key вместо Read-Only обычно не влияет на воспроизведение iframe.

Если Bunny Player открывается, но видео не стартует, проверьте в Bunny Dashboard:

- видео полностью обработано: `encodeProgress=100`, длительность больше 0, есть `availableResolutions`;
- в Stream > Security > Allowed domains добавлен домен Railway без схемы: `web-production-bf9de6.up.railway.app`, а не `https://web-production-bf9de6.up.railway.app`;
- если включена Embed View Token Authentication, в Railway задан `BUNNY_STREAM_EMBED_TOKEN_KEY` из Bunny Security;
- если включена защита HLS/CDN token, сегменты видео тоже должны быть доступны для Bunny Player.

Если Chrome воспроизводит видео, а Safari показывает `playlist.m3u8 403`, это почти всегда означает, что Safari уперся в Bunny Security/CDN ограничения. Для демонстрации проще временно очистить Allowed domains, отключить Block Direct URL File Access и не включать HLS/CDN token protection.
