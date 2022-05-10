#!/bin/bash
check=$(wget -O - -T 2 "http://db:3306" 2>&1 | grep -o 200)
while [ -z "$check" ]; do
    sleep 5s
    check=$(wget -O - -T 2 "http://db:3306" 2>&1 | grep -o 200)
done


flask db init -d data/migrations
flask db migrate -d data/migrations
flask db upgrade -d data/migrations
exec gunicorn -b :5000 --access-logfile - --error-logfile - vmlab:app
