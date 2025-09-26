FROM python:3.10-slim-bullseye

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -U -r requirements.txt
RUN chmod +x start.sh

CMD ["./start.sh"]
