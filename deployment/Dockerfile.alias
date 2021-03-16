# Build Container
FROM python:3.9 as build

WORKDIR /usr/src/app
COPY . .

RUN pip install -r dependencies/requirements-build.txt
RUN python setup.py bdist_wheel

# Execution Container
FROM python:3.9-alpine

RUN adduser --system app

COPY --from=build /usr/src/app/dist /wheels
COPY dependencies/requirements-docker.txt .
RUN pip install --no-cache-dir -r requirements-docker.txt
RUN pip install --no-cache-dir /wheels/*

USER app
CMD ["gunicorn", "alias:create_app()", "--bind", "0.0.0.0:8000"]
