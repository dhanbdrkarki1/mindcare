#!/bin/bash
set -e

# Load environment variables
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-3306}
DB_USER=${DB_USER:-root}
DB_PASS=${DB_PASS:-}
FLASK_APP=${FLASK_APP:-app.py}

# 1. Wait for MySQL to be ready
echo "⏳ Waiting for MySQL at $DB_HOST:$DB_PORT..."
until mysql -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USER" -p"$DB_PASS" -e "SELECT 1" &> /dev/null; do
  sleep 1
done
echo "✅ MySQL is up!"

# # 2. Ensure migrations folder exists
# if [ ! -d "./migrations" ]; then
#   echo "📂 'migrations' folder not found—initializing..."
#   flask db init --directory=migrations
# fi

# # 3. Generate a new migration if models have changed
# echo "📝 Generating migration script..."
# flask db migrate --message "Auto-migration on container start" || \
#   echo "⚠️  No changes detected, skipping 'migrate'."

# # 4. Apply migrations
# echo "🔄 Applying migrations (upgrade)..."
# flask db upgrade

# 5. Start Gunicorn
echo "🚀 Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:5000 app:app