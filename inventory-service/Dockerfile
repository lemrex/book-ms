# Use a smaller, more efficient base image
FROM python:3.11-slim-buster

# Set the working directory
WORKDIR /app

# Install system dependencies (if necessary)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port (adjust as needed)
EXPOSE 3001

# Start the application
CMD ["python", "src/app.py"]
# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:3001", "src.app:app"]
