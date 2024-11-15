FROM python:3.11.5-slim-bullseye

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt 
COPY . /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

