# Base image
FROM python:3.8-slim-buster

# Install git safely and clean cache
RUN apt-get update -o Acquire::CompressionTypes::Order::=gz && \
    apt-get install -y --no-install-recommends git ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Copy start script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Set working directory
RUN mkdir /Auto-filterbot
WORKDIR /Auto-filterbot

# Default command
CMD ["/bin/bash", "/start.sh"]
