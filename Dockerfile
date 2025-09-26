FROM python:3.8-slim-buster

# Fix Buster repository: use archive.debian.org
RUN sed -i 's|http://deb.debian.org/debian|http://archive.debian.org/debian|g' /etc/apt/sources.list \
    && echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid-until \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt /requirements.txt

# Upgrade pip and install dependencies
RUN pip3 install --upgrade pip \
    && pip3 install --upgrade -r /requirements.txt

# Create working directory
RUN mkdir /Auto-filterbot
WORKDIR /Auto-filterbot

# Copy start script
COPY start.sh /start.sh

# Set default command
CMD ["/bin/bash", "/start.sh"]
