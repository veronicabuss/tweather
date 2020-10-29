#!/bin/sh
if [ -z "${VIRTUAL_ENV}" ]; then
  echo "You must activate your virtual environment before running this script. Use: source backend/venv/bin/activate"
else
  flask run
fi
