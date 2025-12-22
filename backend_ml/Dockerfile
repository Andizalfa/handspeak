# Backend ML - BISINDO Sign Language Recognition Service
# TensorFlow + FastAPI + Hugging Face

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY backend_ml/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend_ml/ .

# Create models directory (will be populated from Hugging Face)
RUN mkdir -p models

# Expose port
EXPOSE 8002

# Environment variables (will be overridden by Railway)
ENV HF_REPO_ID="Andizalfa05/handspeak" \
    PORT=8002 \
    PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8002/health || exit 1

# Run the application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]