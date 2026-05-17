#!/bin/sh

# PostgreSQL이 준비될 때까지 대기
echo "Waiting for PostgreSQL..."
while ! pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME; do
  sleep 1
done
echo "PostgreSQL is ready!"

# 데이터베이스 마이그레이션
echo "Running migrations..."
python manage.py migrate --noinput

# 정적 파일 수집
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Gunicorn 서버 시작
echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000