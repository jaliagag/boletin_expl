FROM python:3.11.9-alpine3.19

ARG MDB
ARG PORT

ENV MDB=$MDB
ENV PORT=$PORT

WORKDIR /app
COPY . /app

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8000

CMD [ "sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT" ]
#CMD ["hypercorn", "main:app", "--bind", "[::]:$PORT"]

