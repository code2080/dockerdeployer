FROM python:3.5

WORKDIR /app

ARG GUNICORN_VERSION
ARG REQUIREMENTS

RUN pip install --no-cache-dir gunicorn==$GUNICORN_VERSION

COPY REQUIREMENTS /app/
RUN pip install --no-cache-dir -r REQUIREMENTS

COPY check_connection.py /script/
COPY create_django_admin_user.py /script/

COPY entrypoint.sh /script/
RUN ["chmod", "+x", "/script/entrypoint.sh"]