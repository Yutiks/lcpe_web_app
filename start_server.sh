#!/bin/bash

PROJECT_NAME="lcpe"

PROJECT_DIR="/Users/yusufkholmatov/PycharmProjects/lcpe_web_app/lcpe/"

RUNSERVER_CMD="python3 manage.py runserver"

CELERY_WORKER_CMD="celery -A $PROJECT_NAME worker -l info"
CELERY_BEAT_CMD="celery -A $PROJECT_NAME beat -l info"

cd "$PROJECT_DIR" || exit

echo "🚀 Запуск Django runserver..."
osascript -e 'tell app "Terminal"
    do script "cd '"$PROJECT_DIR"' && '"$RUNSERVER_CMD"'"
end tell'

sleep 2

echo "🔧 Запуск Celery worker..."
osascript -e 'tell app "Terminal"
    do script "cd '"$PROJECT_DIR"' && '"$CELERY_WORKER_CMD"'"
end tell'

sleep 2

echo "⏰ Запуск Celery beat..."
osascript -e 'tell app "Terminal"
    do script "cd '"$PROJECT_DIR"' && '"$CELERY_BEAT_CMD"'"
end tell'

echo "✅ Все процессы запущены!"
