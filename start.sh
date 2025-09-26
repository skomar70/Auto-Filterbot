#!/bin/bash

if [ -z "$UPSTREAM_REPO" ]; then
  echo "Cloning main Repository"
  git clone https://github.com/skomar70/Auto-filterbot.git /Auto-filterbot
  cd /Auto-filterbot
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO"
  git clone "$UPSTREAM_REPO" /AutoFilterAdvance
  cd /AutoFilterAdvance
fi

pip3 install -U -r requirements.txt
echo "Bot Started...."
python3 bot.py
