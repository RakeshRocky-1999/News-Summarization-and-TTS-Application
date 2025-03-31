# Use official Python 3.11 image as base
FROM python:3.11-slim

# Set environment variables to improve performance and avoid bytecode caching
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV TRANSFORMERS_CACHE=/app/cache

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files to the working directory
COPY . /app/

# Create /app/data directory and set permissions
RUN mkdir -p /app/data && chmod -R 777 /app/data

# Create cache directory and set correct permissions
RUN mkdir -p /app/cache && chmod -R 777 /app/cache

# Set correct permissions
USER root

# Expose port for FastAPI (adjust if needed)
EXPOSE 7860

# Run FastAPI application
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7860"]
