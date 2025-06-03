# Use an official Python runtime as a parent image
FROM python:3.13-bookworm

# Set the working directory in the container
WORKDIR /app

# Install system dependencies if any were needed.
# psycopg2-binary (in your requirements.txt) usually bundles necessary libraries,
# so explicit installation of libpq-dev might not be needed.
# Example if it were:
# RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y nano && rm -rf /var/lib/apt/lists/*
# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Using --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the .env file.
# IMPORTANT: For production, it's often better to manage secrets using
# Docker secrets or by passing environment variables at runtime,
# rather than copying the .env file directly into the image.
COPY .env .

# Copy the rest of the application code into the container
COPY ./main.py .
COPY ./app ./app
COPY ./templates ./templates

# Make port 9090 available to the world outside this container (as specified in your main.py)
EXPOSE 9090

# Run main.py when the container launches
CMD ["python", "main.py"]