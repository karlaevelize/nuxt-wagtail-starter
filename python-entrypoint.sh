#!/usr/bin/env sh
set -e # Exit on error

echo "Creating virtual environment..."
python -m venv ./var/venv

echo "Installing dependencies..."
python -m pip install -U pip
python -m pip install -r ./requirements_local.txt

if [ ! -f './content/local.ini' ]; then
    echo "Creating local.ini..."
    cp './content/local.example.ini' './content/local.ini'
fi

# NOTE: To debug issues with the container, without starting the server,
#       run the container with the argument "debug-container".
if [ "${1}" = "debug-container" ]; then
  echo "Sleeping forever..."
  sleep infinity
fi

echo "Migrating database..."
python ./manage.py migrate

echo "Starting server..."
exec python -W module ./manage.py runserver 0:"${DJANGO_RUNSERVER_PORT:-8000}"
