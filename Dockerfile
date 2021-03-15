# Build Container
FROM python:3.9 as build

WORKDIR /usr/src/app
COPY . .

RUN pip install -r dependencies/requirements-dist.txt
RUN python setup.py bdist_wheel

# Execution Container
FROM python:3.9-slim

RUN adduser --system app

COPY --from=build /usr/src/app/dist /wheels
RUN pip install --no-cache /wheels/*

USER app
