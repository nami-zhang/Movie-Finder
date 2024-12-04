# Use the official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY app /app

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose Flask port
EXPOSE 5000

# Command to start the Flask app
CMD ["python", "/app/app.py"]
