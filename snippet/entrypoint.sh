#!/bin/bash

set -e  # Остановить выполнение при ошибке

# Функция для проверки готовности базы данных
wait_for_db() {
  echo "Waiting for database to be ready..."
  while ! nc -z $DB_HOST $DB_PORT; do
    sleep 1
  done
  echo "Database is ready!"
}

# Ждём, пока база данных будет готова
wait_for_db

# Применяем миграции
echo "Applying database migrations..."
python manage.py migrate

# Создаем суперпользователя (если он еще не создан)
echo "Creating superuser..."
python create_superuser.py


# Запускаем основное приложение
echo "Starting Gunicorn server..."
exec gunicorn snippet.wsgi:application --bind 0.0.0.0:8000