#!/bin/bash
set -e

# 0. Launch Nginx in the background
echo "🔀 Starting Nginx..."
nginx -t  # Test the configuration
service nginx start  # Start as a service instead of directly

# Load env defaults
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-3306}
DB_USER=${DB_USER:-root}
DB_PASS=${DB_PASS:-}
FLASK_APP=${FLASK_APP:-app.py}

# 1. Wait for MySQL
echo "⏳ Waiting for MySQL at $DB_HOST:$DB_PORT..."
until mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASS" -e "SELECT 1" &>/dev/null; do
  sleep 1
done
echo "✅ MySQL is up!"

# 2. (migrations if you re-enable them…)

# 3. Start Gunicorn in the foreground
echo "🚀 Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:5000 app:app
