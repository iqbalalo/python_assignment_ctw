FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y

WORKDIR /financial

ADD ./financial /financial

COPY ./requirements.txt /financial
RUN pip install -r requirements.txt

EXPOSE 8000