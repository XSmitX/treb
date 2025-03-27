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
RUN echo 'import socket\n\
import threading\n\
import time\n\
\n\
def tcp_health_check():\n\
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n\
    server.bind(("0.0.0.0", 8000))\n\
    server.listen(1)\n\
    print("TCP Health check server listening on port 8000")\n\
    while True:\n\
        try:\n\
            client, addr = server.accept()\n\
            client.close()\n\
        except Exception as e:\n\
            print(f"Health check error: {e}")\n\
\n\
def start_health_check():\n\
    health_thread = threading.Thread(target=tcp_health_check, daemon=True)\n\
    health_thread.start()\n\
    print("Health check thread started")\n\
\n\
if __name__ == "__main__":\n\
    start_health_check()\n\
    while True:\n\
        time.sleep(1)\n\
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
