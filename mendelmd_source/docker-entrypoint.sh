#!/bin/bash

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"#
python manage.py migrate auth
python manage.py migrate

export C_FORCE_ROOT='true'
# Start server
echo "Starting annotator"
python manage.py celery worker -c 4 &
# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000 