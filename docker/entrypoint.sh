#!/bin/sh
set -e

if [ -n "$POSTGRES_DB" ]; then
  echo "Aguardando Postgres em $POSTGRES_HOST:$POSTGRES_PORT..."
  while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
    sleep 1
  done
fi

python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py criar_dados_demo

exec "$@"
