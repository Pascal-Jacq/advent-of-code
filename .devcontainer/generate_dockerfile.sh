#!/usr/bin/env bash
IMAGENAME=$1
FILENAME=Dockerfile

if [[ ! -f $FILENAME ]]
then
    echo "Generating default $FILENAME"
    cat <<EOL > $FILENAME
FROM python:3.11-slim

# Just need ps to handle container lifetime
RUN apt-get update && apt-get install -y procps git --no-install-recommends && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install -r requirements.txt
EOL
fi

docker build -t $IMAGENAME .
