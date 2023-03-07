# syntax=docker/dockerfile:1

FROM python:3.8.3-slim

WORKDIR /broker_manager_docker
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 5000
EXPOSE 7000-8000

CMD [ "python", "app.py"]
.0000000000
