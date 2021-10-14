FROM python:3.8-slim-buster
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
WORKDIR /app/dining_hall_api

EXPOSE 5001
CMD ["python", "dining_hall.py"]