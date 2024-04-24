FROM python:3.11.9-alpine3.19

ARG MDB
ENV MDB=$MDB

WORKDIR /app
COPY . /app

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 5000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]


