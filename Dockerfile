# First stage: Build
FROM python:3.12-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip3 install poetry==1.8.3

WORKDIR /code

COPY pyproject.toml poetry.lock /code/

# Second stage: Run
FROM python:3.12-slim

WORKDIR /code

COPY --from=builder /usr/local /usr/local
COPY . /code/

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi