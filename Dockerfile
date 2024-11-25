# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . /app
EXPOSE 5000
# Install dependencies
RUN pip install flask mysql-connector-python

# Command to run the application
CMD ["python", "app.py"]

