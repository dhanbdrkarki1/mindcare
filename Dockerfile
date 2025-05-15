# Dockerfile
FROM python:3.10-slim

# Install OS packages: MySQL client + Nginx & supervisor deps
RUN apt-get update \
    && apt-get install -y \
    default-mysql-client \
    procps \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app + entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
COPY . /app

# Expose the HTTP port
EXPOSE 80

# Entrypoint will start Nginx, wait for MySQL, then Gunicorn
ENTRYPOINT ["/entrypoint.sh"]
