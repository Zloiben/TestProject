# !/bin/bash
set -e

. ./.env

if [ "$MODE" = "PROD" ]; then
    echo "Запуск боевого режима"
    exec uvicorn main:app --host 0.0.0.0 --port 8000
else
   echo "Тестирования..."
fi