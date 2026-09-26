# Production image for Render (see render.yaml at the repo root).
# Build stage compiles mysqlclient; the final image only carries its runtime library.

FROM python:3.13-slim AS build
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential pkg-config default-libmysqlclient-dev \
 && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
RUN apt-get update \
 && apt-get install -y --no-install-recommends libmariadb3 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY --from=build /wheels /wheels
RUN pip install --no-cache-dir /wheels/* && rm -rf /wheels

COPY . .

# Static files are collected at build time; settings only need a placeholder key for this.
RUN DEBUG=false SECRET_KEY=collectstatic-only python manage.py collectstatic --noinput

# Unprivileged runtime user.
RUN useradd --create-home app && chown -R app /app
USER app

# Render sets PORT. Migrations are a no-op once the database is loaded, but keep
# new ones applied on each deploy. Two workers fit the free plan's 512 MB.
CMD ["sh", "-c", "python manage.py migrate --noinput && exec gunicorn st_anthony.wsgi:application --bind 0.0.0.0:${PORT:-10000} --workers 2 --threads 2 --timeout 60 --access-logfile -"]
