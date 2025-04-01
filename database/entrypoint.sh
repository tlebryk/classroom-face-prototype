#!/bin/bash
set -e

echo "Setting up the database..."
python /app/setup_db.py

echo "Starting database service..."
exec gunicorn -b 0.0.0.0:5002 app:app
