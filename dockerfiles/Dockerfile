# Use an appropriate base image for your application
FROM python:3.9-alpine

# Install system dependencies
RUN apk add --no-cache \
    mesa-gl \
    libffi-dev \
    # Add other dependencies if needed

# Install Python dependencies
RUN pip install --no-cache-dir \
    deepface \
    opencv-python-headless \
    # Add other Python dependencies if needed

# Copy your application code
COPY . /app

# Set the working directory
WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your application will run on
EXPOSE 8000

# Start your application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
