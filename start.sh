if [ -z $UPSTREAM_REPO ]
then
  echo "Cloning main Repository"
  git clone https://github.com/skomar70/AutoFilterbot /AutoFilterbot
else
  echo "Cloning Custom Repo from $UPSTREAM_REPO "
  git clone $UPSTREAM_REPO /AutoFilterAdvance
fi
cd /AutoFilterbot
pip3 install -U -r requirements.txt
echo "Bot Started...."
python3 bot.py
