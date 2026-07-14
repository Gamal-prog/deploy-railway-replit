web: python manage.py migrate --noinput && python manage.py ensure_demo_admin && python manage.py collectstatic --noinput && gunicorn projectConfig.wsgi:application --bind 0.0.0.0:$PORT
