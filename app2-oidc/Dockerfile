# Dockerfile for OIDC Application Backend
# Based on Python 3.11 slim image for minimal footprint
# Simpler than SAML as OIDC doesn't require system-level XML libraries

FROM python:3.11-slim

# Set working directory for the application
WORKDIR /app

# Copy requirements file first for better Docker layer caching
COPY backend/requirements.txt .

# Install Python dependencies
# OIDC libraries are pure Python, no system dependencies needed
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend/ .

# Ensure Python output is sent straight to terminal without buffering
# Important for real-time logging in containerized environments
ENV PYTHONUNBUFFERED=1

# Expose Flask application port
EXPOSE 5000

# Run the Flask application
# In production, consider using a WSGI server like Gunicorn
CMD ["python", "app.py"]