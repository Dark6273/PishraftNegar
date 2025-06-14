#!/bin/sh

echo "Migrating database..."
python manage.py migrate --noinput

echo "Starting server..."
gunicorn --bind "0.0.0.0:8000" --workers 1 --timeout 120 core.wsgi:application
