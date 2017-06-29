FROM ubuntu:16.04

RUN apt-get update

RUN apt-get install -y python3

RUN apt-get install -y python3-numpy

RUN apt-get install -y python3-mysql.connector

RUN apt-get install -y wget

WORKDIR /app

COPY . /app/

RUN wget https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh
RUN chmod +x wait-for-it.sh

EXPOSE 5555

CMD ["python3","test_query.py"]
