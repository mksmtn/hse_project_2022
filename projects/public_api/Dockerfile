FROM python:3.8

WORKDIR /app

COPY ./lfm-b2 /lfm-b2

RUN pip install pipenv

COPY ./Pipfile ./Pipfile.lock /app

RUN pipenv install --system --deploy

COPY ./pickle /app/pickle

COPY ./src /app/src

CMD ["uvicorn", "src.server:create_app", "--host", "0.0.0.0", "--port", "80"]
