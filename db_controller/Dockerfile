FROM ubuntu:16.04

RUN apt-get update

RUN apt-get install -y python3

RUN apt-get install -y python3-numpy

RUN apt-get install -y python3-mysql.connector

WORKDIR /app

COPY insert_query.py /app/insert_query.py

COPY propagation_model_estimation.py /app/propagation_model_estimation.py

COPY query_data.py /app/query_data.py

COPY test_query.py /app/test_query.py

EXPOSE 5555 

CMD ["python3","test_query.py"]