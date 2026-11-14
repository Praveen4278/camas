# Multi-stage build for CAMAS platform

# Stage 1: Frontend build
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend files
COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ ./

# Build frontend
RUN npm run build

# Stage 2: Backend with Python
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy backend dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY app.py .
COPY config/ config/
COPY agents/ agents/
COPY database/ database/
COPY experiments/ experiments/
COPY prompts/ prompts/ 2>/dev/null || true

# Copy built frontend from stage 1
COPY --from=frontend-builder /app/frontend/dist frontend/dist

# Create necessary directories
RUN mkdir -p reports visualizations database

# Expose ports
EXPOSE 8000 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start command
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
