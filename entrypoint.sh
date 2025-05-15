#!/bin/bash
set -e

# Start Gunicorn in the foreground
echo "🚀 Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:5000 app:app
