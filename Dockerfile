FROM python:3.8-slim-buster

# Fix old Debian repository
RUN sed -i 's|http://deb.debian.org/debian|http://archive.debian.org/debian|g' /etc/apt/sources.list \
    && echo 'Acquire::Check-Valid-Until "false";' > /etc/apt/apt.conf.d/99no-check-valid-until \
    && apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt /requirements.txt
RUN pip3 install --upgrade pip \
    && pip3 install --upgrade -r /requirements.txt

# Set working directory and clone repo
WORKDIR /Auto-filterbot
RUN git clone https://github.com/skomar70/Auto-filterbot.git /Auto-filterbot

# Copy start script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Run the bot on container start
CMD ["/bin/bash", "/start.sh"]
