FROM node:18 AS nodejs

WORKDIR /app

# cron wants to put its PID tracking file in /var/run and it's running
# under the app user, so the directory must be writeable by that user.
RUN mkdir -p /var/run && chown app:app /var/run

COPY frontend/package.json frontend/package-lock.json ./

RUN --mount=type=cache,target=/root/.npm \
    npm install --loglevel verbose

COPY frontend frontend/
COPY templates templates/
COPY techcity/core/frontend.py techcity/core/

RUN npm --prefix frontend run css

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_PROJECT_ENVIRONMENT=/usr/local

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        cron \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.4.7 /uv /bin/uv

WORKDIR /app

RUN addgroup --gid 222 --system app \
    && adduser --uid 222 --system --group app

RUN mkdir -p /app && chown app:app /app

COPY --chown=app:app pyproject.toml uv.lock /app/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

COPY --chown=app:app . /app/

COPY --from=nodejs /app/static/site.css static/

RUN \
    SECRET_KEY=builder-secret \
    python manage.py collectstatic --noinput

USER app

EXPOSE 8000

CMD ["gunicorn", "project.wsgi", "--workers=2", "--log-file=-", "--bind=0.0.0.0:8000"]
