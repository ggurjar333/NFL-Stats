# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app/ loveofsports_nfl /app/ init.sh /app/ run.sh /app/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make the script executable
RUN chmod +x /app/init.sh

# Run the bash script when the container launches
CMD ["/bin/bash", "/app/init.sh"]





# Expose the port that Dagster runs on (default is 3000)
EXPOSE 3000

# Define environment variable
ENV DAGSTER_HOME /app/dagster_home

# Run app.py when the container launches
CMD ["dagit", "-h", "0.0.0.0"]
