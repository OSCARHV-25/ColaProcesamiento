
FROM python:3.9-slim


WORKDIR /app


 COPY . /app/


RUN pip install flask

RUN pip install pika

RUN pip install mysql-connector-python


EXPOSE 5000


CMD ["python", "productor.py"]