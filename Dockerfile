# Use an official Python runtime as a parent image
FROM python:3.11.5

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y unixodbc unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /project

# Copy the requirements file into the container at /app
COPY requirements.txt /project/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /project/


# Expose the port the app runs on
EXPOSE 8001

# Command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
