# Use a small Python base image
FROM python:3.9-slim

# Install ffmpeg and any system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
           ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Create a directory for the app
WORKDIR /app

# Copy Python dependencies file and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app and templates
COPY app.py .
COPY templates/ templates/

# Expose port 5000 for Flask
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
