COPY python:3.10

WORKDIR /app

COPY ./requirements.txt /code

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./src /app/src

WORKDIR /app/src

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]
