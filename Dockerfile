FROM colesbury/python-nogil
#FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED=1
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
WORKDIR /app/dining_hall_api

EXPOSE 5000
CMD ["python", "dining_hall.py"]