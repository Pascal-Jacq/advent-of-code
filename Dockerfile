FROM python:3.11-slim

# Just need ps to handle container lifetime
RUN apt-get update && apt-get install -y procps --no-install-recommends && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt
