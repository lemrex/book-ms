# # Use a lightweight Python image
# FROM python:3.11-slim

# # Set working directory
# WORKDIR /app

# # Install dependencies
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the application code
# COPY . .

# # Expose the port (update as per your app's configuration)
# EXPOSE 3001

# # Start the application
# CMD ["python", "src/inventory.py"]

# Use a lightweight Python image
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port (update as per your app's configuration)
EXPOSE 3001

# Start the application
CMD ["python", "src/app.py"]

