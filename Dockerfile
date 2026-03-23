# --- MULTI-STAGE DOCKER SETUP FOR INTERVIEWAI ---

# 1. FRONTEND BUILDER
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# 2. BACKEND PRODUCTION
FROM python:3.11-slim
WORKDIR /app

# Ensure standard system tools
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Backend Dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ .

# Copy frontend build from previous stage (for static serving if needed)
COPY --from=frontend-builder /app/frontend/dist ./static

# Expose FastAPI Port
EXPOSE 8000

# Entrypoint
CMD ["python", "main.py"]