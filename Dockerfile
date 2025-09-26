# Base image
FROM python:3.8-slim-buster

# Avoid broken apt repositories, install git safely
RUN apt-get update -o Acquire::CompressionTypes::Order::=gz && \
    apt-get install -y --no-install-recommends git ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt /requirements.txt

# Upgrade pip and install dependencies
RUN pip3 install --upgrade pip && pip3 install --upgrade -r /requirements.txt

# Create working directory
RUN mkdir /Auto-filterbot
WORKDIR /Auto-filterbot

# Copy start script
COPY start.sh /start.sh

# Set default command
CMD ["/bin/bash", "/start.sh"]
