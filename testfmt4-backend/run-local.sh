#!/bin/bash
source ./venv/bin/activate
FLASK_APP="app.py" FLASK_ENV=development FLASK_DEBUG=1 flask run
deactivate

