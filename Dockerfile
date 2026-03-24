FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy configuration files
COPY requirements.txt .
COPY pyproject.toml .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY config.py .

# Environment variables
ENV PYTHONPATH=/app
ENV EASYPANEL_URL=""
ENV EASYPANEL_API_KEY=""
ENV PORT=8080
ENV MCP_HOST=0.0.0.0

# Expose port
EXPOSE 8080

# Run the server in HTTP mode for remote access
# Using -u to ensure logs are flushed immediately
CMD ["python", "-u", "src/server.py", "http"]
