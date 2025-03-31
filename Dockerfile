# Use official Python 3.11-slim image as base (lightweight)
FROM python:3.11-slim

# Set environment variables to improve performance and avoid bytecode caching
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TRANSFORMERS_CACHE=/app/cache

# Set the working directory
WORKDIR /app

# Install system-level dependencies required by some packages
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies in a separate step for caching
COPY requirements.txt /app/

# Use pip cache for better performance
RUN pip install --no-cache-dir -r requirements.txt

# Create cache and data directories with correct permissions
RUN mkdir -p /app/cache /app/data && chmod -R 777 /app/cache /app/data

# Copy all project files AFTER installing dependencies (to leverage Docker cache)
COPY . /app/

# Switch to non-root user for security (optional but recommended)
# USER 1001

# Expose port for FastAPI (adjust if needed)
EXPOSE 7860

# Run FastAPI application with multiple workers for better performance
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "4"]

