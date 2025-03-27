# Use the official Python image as the base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file first to leverage Docker cache for faster rebuilds
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot.py file into the container
COPY bot.py .

# Expose a port (optional, if you have an HTTP server or want to run a service on a port)
EXPOSE 8080

# Create a non-root user for better security
RUN useradd -m -u 1000 botuser && \
    chown -R botuser:botuser /app

# Switch to the non-root user
USER botuser

# Command to run the bot
CMD ["python", "bot.py"]
