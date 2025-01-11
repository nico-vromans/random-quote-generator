#!/bin/bash

args=( "${@:1}" )

echo "Apply migrations..."
python manage.py migrate --database default --no-input --no-color

echo "Collect static files..."
python manage.py collectstatic --no-input --no-color

echo "Flushing endpoint cache..."
python manage.py flush_endpoint_cache "/*" --no-color

echo "Running server (args: ${args[*]})..."
export GUNICORN_CMD_ARGS="${args[*]}"
python -m gunicorn rqg.wsgi:application
