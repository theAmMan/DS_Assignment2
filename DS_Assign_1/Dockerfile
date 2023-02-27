# syntax=docker/dockerfile:1

FROM python:3.8.3-slim

WORKDIR /assgn1

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# ENTRYPOINT ["python","create_database.py"]

CMD [ "python", "manage.py" , "runserver"]