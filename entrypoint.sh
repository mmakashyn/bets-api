#!/bin/sh

#debug logs
echo "Starting CORE API..."

# Function to check if the PostgresSQL database is available
postgres_ready() {
python << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="${DATABASE_NAME}", user="${DATABASE_USER}", password="${DATABASE_PASSWORD}", host="${DATABASE_HOST}", port="${DATABASE_PORT}", options="-c statement_timeout=300000")
except psycopg2.OperationalError:
    sys.exit(-1)
sys.exit(0)
END
}

# Check once a second if the DB is available
until postgres_ready; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

# Apply migrations
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --no-input
python3 manage.py runserver 0.0.0.0:8000
