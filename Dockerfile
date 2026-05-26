# ==========================================
# AI Study Buddy Pro - Dockerfile
# ==========================================

# Use lightweight official Python image
FROM python:3.11-slim

# ==========================================
# Environment Variables
# ==========================================

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Prevent Python buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

# Streamlit configuration
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# ==========================================
# Set Working Directory
# ==========================================

WORKDIR /app

# ==========================================
# Install System Dependencies
# ==========================================

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ==========================================
# Copy Requirements File
# ==========================================

COPY requirements.txt .

# ==========================================
# Install Python Dependencies
# ==========================================

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ==========================================
# Copy Application Files
# ==========================================

COPY . .

# ==========================================
# Expose Streamlit Port
# ==========================================

EXPOSE 8501

# ==========================================
# Health Check
# ==========================================

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# ==========================================
# Run Streamlit Application
# ==========================================

CMD ["streamlit", "run", "app/app.py"]