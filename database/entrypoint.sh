#!/bin/bash
set -e

# Initialize the database
python -c "from app import init_db; init_db()"

# Start Gunicorn
exec gunicorn -b 0.0.0.0:5002 app:app
