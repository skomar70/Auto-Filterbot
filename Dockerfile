FROM python:3.8-slim-buster

# Avoid interactive prompts, update package lists, fix missing dependencies, upgrade safely
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt /requirements.txt

# Upgrade pip and install python dependencies
RUN pip install --upgrade pip && pip install --upgrade -r /requirements.txt

# Create working directory
RUN mkdir /Auto-filterbot
WORKDIR /Auto-filterbot

# Copy start script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Default command
CMD ["/bin/bash", "/start.sh"]
