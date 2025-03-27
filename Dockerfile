# Use the official Python image as the base
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements first to leverage Docker cache for faster rebuilds
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the bot.py file into the container
COPY bot.py .

# Create a non-root user for better security
RUN useradd -m -u 1000 botuser && \
    chown -R botuser:botuser /app

# Switch to non-root user
USER botuser

# Verify files exist (Optional for debugging)
RUN ls -la /app

# Command to run the bot
CMD ["python", "bot.py"]
