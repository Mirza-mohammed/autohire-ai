# Use the official Microsoft Playwright image as the base so we don't have to manually install browser dependencies
FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# We don't need to run `playwright install` because the base image already has the browsers!

# Copy project
COPY . /app/

# Expose port for FastAPI
EXPOSE 8000

# Entrypoint will be defined in docker-compose.yml so we can reuse this image for the Worker
