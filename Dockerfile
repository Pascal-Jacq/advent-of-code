FROM python:3.12-slim

# Just need ps to handle container lifetime
RUN apt-get update && apt-get install -y procps ssh wget curl git --no-install-recommends && rm -rf /var/lib/apt/lists/*

WORKDIR /install
COPY requirements.txt /install/
RUN pip install -r requirements.txt && rm requirements.txt
ENV PYTHONPATH=/install/

COPY *.py template.ipynb /install/
