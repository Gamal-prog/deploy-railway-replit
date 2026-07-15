# Experience Instructions

## Railway + Django: Application Failed To Respond

Context from this project: Django MVP deployed to Railway showed:

```text
Application failed to respond
This error appears to be caused by the application.
```

There were no useful Django errors in logs. Database was connected, migrations passed, and environment variables were set. The actual issue was ambiguity around how Railway started the app and which port the public domain targeted.

## What Fixed It

Use one explicit startup script and force Railway to use it.

Required files:

- `bin/start`
- `railway.json`
- `Procfile`
- `Dockerfile`

The startup script must:

- print the selected port;
- run migrations;
- optionally create the demo admin;
- collect static files;
- start Gunicorn on `0.0.0.0:${PORT}`.

Example:

```sh
#!/usr/bin/env sh
set -eu

PORT="${PORT:-8000}"

echo "lectureLib startup"
echo "PORT=${PORT}"

python manage.py migrate --noinput
python manage.py ensure_demo_admin
python manage.py collectstatic --noinput

echo "Starting gunicorn on 0.0.0.0:${PORT}"
exec gunicorn projectConfig.wsgi:application \
  --bind "0.0.0.0:${PORT}" \
  --workers "${WEB_CONCURRENCY:-2}" \
  --access-logfile - \
  --error-logfile - \
  --capture-output
```

Railway config:

```json
{
  "$schema": "https://railway.com/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "sh bin/start",
    "healthcheckPath": "/health/",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

## Railway Settings Checklist

In Railway service variables:

```env
PORT=8000
DEBUG=False
DJANGO_ALLOWED_HOSTS=.up.railway.app,.railway.app
CSRF_TRUSTED_ORIGINS=https://*.up.railway.app,https://*.railway.app
SECRET_KEY=<real-secret-key>
```

If using Railway Postgres, make sure the web service receives either:

- `DATABASE_URL`, or
- `PGDATABASE`, `PGUSER`, `PGPASSWORD`, `PGHOST`, `PGPORT`.

In Railway Networking:

```text
Target port: 8000
```

The target port must match the port printed by `bin/start`.

## Logs To Look For

After deploy, logs must include:

```text
lectureLib startup
PORT=8000
Starting gunicorn on 0.0.0.0:8000
Listening at: http://0.0.0.0:8000
```

If these lines are missing, Railway is probably not running the intended start command.

Check:

- Railway service Settings does not override Start Command incorrectly.
- `railway.json` is committed and pushed.
- `bin/start` is committed and executable.
- the latest deployment uses the latest commit.

## Diagnostic Rule

If:

- migrations pass;
- database connection works;
- no Python traceback appears;
- Railway still shows `Application failed to respond`;

then suspect startup/port routing first, not Django views or database models.

Most likely causes:

- app listens on one port, Networking points to another;
- app listens on `127.0.0.1` instead of `0.0.0.0`;
- Railway chose a different startup path (`Dockerfile`, `Procfile`, Nixpacks default);
- manual Railway Start Command overrides repository config;
- healthcheck points to a missing or slow endpoint.

## Good Pattern For Future Django MVP Deploys

Always add:

- `/health/` endpoint returning `200 OK`;
- explicit `bin/start`;
- explicit `railway.json`;
- Gunicorn bind to `0.0.0.0:${PORT:-8000}`;
- logs that print the port before Gunicorn starts;
- `WhiteNoiseMiddleware` for static files;
- Postgres support via `DATABASE_URL` and Railway `PG*` variables.

This removes most of the guesswork from Railway deploys.

## Bunny Stream Playback Checklist

If Bunny metadata appears on the page but the player stays at `0:00`, do not switch to a full API key first.

`BUNNY_STREAM_API_KEY` / Read-Only AccessKey is used only by Django for `GET /library/{libraryId}/videos/{videoId}`. If title and description are visible, that request already works. The iframe playback is controlled by Bunny Stream processing and Security settings.

Check Bunny Dashboard:

- the video is fully processed: `encodeProgress=100`, duration is greater than 0, and `availableResolutions` is not empty;
- Stream > Security > Allowed domains contains the Railway domain without scheme: `web-production-bf9de6.up.railway.app`, not `https://web-production-bf9de6.up.railway.app`;
- if Embed View Token Authentication is enabled, set `BUNNY_STREAM_EMBED_TOKEN_KEY` on Railway using the Bunny token security key;
- if CDN/HLS token protection is enabled, playlist and segment files must be authorized too.

The app supports signed embed URLs. When `BUNNY_STREAM_EMBED_TOKEN_KEY` is present, player URLs include `token` and `expires`.
