#!/bin/bash

# Collect static files
# echo "Collect static files"
# python3 manage.py collectstatic --noinput

# # Apply database migrations
# echo "Apply database migrations"#
# python3 manage.py migrate auth
# python3 manage.py migrate

export C_FORCE_ROOT='true'
# Start server
echo "Starting annotator"
python3 manage.py celery beat &
python3 manage.py celery worker -c 4 -l debug &
# Start server
echo "Starting server"
python3 manage.py runserver 0.0.0.0:8000 