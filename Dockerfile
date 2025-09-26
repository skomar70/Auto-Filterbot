FROM python:3.10-slim

# Avoid warnings by setting noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Update package lists and install git safely
RUN apt-get update \
    && apt-get install -y --no-install-recommends git curl wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]
