#!/bin/sh
if [ -z "${VIRTUAL_ENV}" ]; then
	echo "You must activate your virtual environment before running this script. Use: source backend/venv/bin/activate"
else
	export FLASK_APP=backend/run.py 
	export FLASK_DEBUG=1
	flask run
fi
