#!/bin/bash

# Update package list
apt-get update

# Install ODBC Driver 17 for SQL Server
apt-get install -y curl gnupg2 unixodbc-dev

# Download and install Microsoft's ODBC Driver 17
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Run the FastAPI application
uvicorn main:app --host 0.0.0.0 --port $PORT
