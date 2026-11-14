 # Multistage build 
 # stage 1: build stage 
FROM python:3.8-slim as Build

# Setting the directory the application will live in 
WORKDIR /app

# Intsalling dependancies for mysql image 
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libmariadb-dev \
    pkg-config

# Copy the files. (first dot, the directory our files are in. Second dot where in our container we would like to store it) 
COPY . .

# Install files 
RUN pip install flask mysqlclient

# stage 2 : production stage 

# Start from python slim image
FROM python:3.8-slim

# Working directory for application in image 
WORKDIR /app

# Copy necesary files from build,
RUN apt-get update && apt-get install -y libmariadb3
COPY --from=build /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=build /app /app 

# Select the port
EXPOSE 5002

# Run the container
CMD ["python", "app.py"]