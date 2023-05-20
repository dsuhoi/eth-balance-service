FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev

ENV PYTHONUNBUFFERED 1

COPY manage.py requirements.txt pytest.ini ./
COPY balance_api/ ./balance_api/
COPY eth_service/ ./eth_service/

RUN pip3 install -r requirements.txt
RUN python3 manage.py makemigrations
