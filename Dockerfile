# Use the official Python image as a base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Update the package lists and install libglib2.0-dev, and Tkinter dependencies
RUN apt-get update && apt-get install -y libglib2.0-dev tk-dev

# Set the environment variables
ENV SDL_AUDIODRIVER="dummy"
ENV DISPLAY=host.docker.internal:0.0

# Install Python dependencies from requirements.txt
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Run pytest to test the application
RUN python3 -m pytest --cov-report html --cov .

# Set the command to run your application
CMD ["python3", "./gui.py"]
