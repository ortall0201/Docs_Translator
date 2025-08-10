# Use Python 3.13 slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies for PyMuPDF and health checks
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Create directories for uploads and outputs
RUN mkdir -p uploads outputs

# Expose port
EXPOSE 8000

# Add health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the FastAPI server
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]