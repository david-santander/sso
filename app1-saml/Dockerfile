# Dockerfile for SAML Application Backend
# Based on Python 3.11 slim image for minimal footprint
# Includes xmlsec dependencies required for SAML authentication

FROM python:3.11-slim

# Set working directory for the application
WORKDIR /app

# Install system dependencies required for python3-saml/xmlsec
# These are necessary for SAML signature validation and encryption
RUN apt-get update && apt-get install -y \
    gcc \                      # C compiler for building Python extensions
    g++ \                      # C++ compiler for building Python extensions
    pkg-config \               # Helper tool for compiling applications
    libxml2-dev \              # XML parsing library development files
    libxmlsec1-dev \           # XML security library development files
    libxmlsec1-openssl \       # OpenSSL backend for xmlsec
    libxslt1-dev \             # XSLT library development files
    && rm -rf /var/lib/apt/lists/*  # Clean up apt cache to reduce image size

# Copy requirements file first for better Docker layer caching
COPY backend/requirements.txt .

# Install Python dependencies with specific versions
# Installing lxml and xmlsec separately ensures compatibility
RUN pip install --no-cache-dir lxml==4.9.3 && \ # XML processing library
    pip install --no-cache-dir xmlsec==1.3.13 && \   # XML security bindings for SAML
    pip install --no-cache-dir -r requirements.txt    # Remaining dependencies

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