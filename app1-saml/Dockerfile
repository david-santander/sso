FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for xmlsec
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    pkg-config \
    libxml2-dev \
    libxmlsec1-dev \
    libxmlsec1-openssl \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .

# Install dependencies with specific versions to avoid conflicts
RUN pip install --no-cache-dir lxml==4.9.3 && \
    pip install --no-cache-dir xmlsec==1.3.13 && \
    pip install --no-cache-dir -r requirements.txt

COPY backend/ .

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "app.py"]