FROM python:3.9-buster

RUN apt-get update -y

RUN mkdir /app
COPY src/requirements.txt /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY src /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD [ "python", "-u", "filegen_consumer.py" ]