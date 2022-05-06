#!/bin/bash
flask db init -d data/migrations
flask db migrate -d data/migrations
flask db upgrade -d data/migrations
exec gunicorn -b :5000 --access-logfile - --error-logfile - vmlab:app
