FROM python:3.10-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update \
    && apt-get install -y default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy entrypoint and app code
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY . .

# Set environment variables (these can be overridden by Docker Compose)
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 5000

# Use entrypoint to run migrations then start Gunicorn
ENTRYPOINT ["/entrypoint.sh"]