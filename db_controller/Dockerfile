FROM ubuntu:16.04

RUN apt-get update

RUN apt-get install -y python3

RUN apt-get install -y python3-numpy

RUN apt-get install -y python3-mysql.connector

WORKDIR /app

COPY . /app/



EXPOSE 5555 

CMD ["python3","test_query.py"]