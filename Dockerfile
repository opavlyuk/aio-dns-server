# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /pyhole/

# Copy the current directory contents into the container at /app
COPY . /pyhole/

# Copy config
COPY ./config.yml /config.yml

# Install any needed packages specified in requirements.txt
RUN pip install -e .

EXPOSE 53/udp

# Run app.py when the container launches
CMD aio-dns-server