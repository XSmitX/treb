# Use the official Python image as the base
FROM python:3.9-slim

# Set the working directory in the container (root directory)
WORKDIR /

# Copy all files from the current directory (where the Dockerfile is located) to the container's root directory
COPY . .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose a port (optional, only needed if your app uses a network port)
EXPOSE 8080

# Command to run the bot
CMD ["python", "bot.py"]
