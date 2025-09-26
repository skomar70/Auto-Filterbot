#!/bin/bash

# Check if UPSTREAM_REPO is set
if [ -z "$UPSTREAM_REPO" ]; then
    echo "Cloning main Repository..."
    git clone https://github.com/skomar70/Auto-filterbot.git /Auto-filterbot
else
    echo "Cloning custom repository from $UPSTREAM_REPO..."
    git clone "$UPSTREAM_REPO" /Auto-filterbot
fi

# Go to working directory
cd /Auto-filterbot || { echo "Failed to cd into /Auto-filterbot"; exit 1; }

# Install dependencies
pip3 install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip3 install -U -r requirements.txt
fi

# Start bot
echo "Bot Started...."
if [ -f "bot.py" ]; then
    python3 bot.py
else
    echo "Error: bot.py not found"
    exit 1
fi
