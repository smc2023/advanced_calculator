FROM python:3.11-slim

# Create and use app directory
WORKDIR /app

# Copy project files into the image
COPY . /app

# Expose the port used by server.py
EXPOSE 8080

# Run the Python HTTP server
CMD ["python", "server.py"]

