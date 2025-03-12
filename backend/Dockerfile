FROM  python:3.12.3

ENV PYTHONUNBUFFERED=1

WORKDIR /api

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . . 
