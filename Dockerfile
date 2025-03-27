# Use the official Python image as the base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Create and set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all Python files
COPY *.py .

# Create a simple health check script
RUN echo 'from http.server import HTTPServer, BaseHTTPRequestHandler\n\
class HealthCheckHandler(BaseHTTPRequestHandler):\n\
    def do_GET(self):\n\
        self.send_response(200)\n\
        self.end_headers()\n\
        self.wfile.write(b"OK")\n\
\n\
def run_health_check():\n\
    server = HTTPServer(("0.0.0.0", 8000), HealthCheckHandler)\n\
    server.serve_forever()\n\
' > health_check.py

# Debug: List all files in the working directory
RUN echo "Files in /app:" && ls -la /app

# Create a non-root user
RUN useradd -m -u 1000 botuser && \
    chown -R botuser:botuser /app

# Switch to non-root user
USER botuser

# Expose the health check port
EXPOSE 8000

# Start both the health check server and the bot
CMD ["sh", "-c", "python health_check.py & python bot.py"] 
