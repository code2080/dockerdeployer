FROM python:3.6

WORKDIR /app

ARG GUNICORN_VERSION
ARG REQUIREMENTS
ARG SETTINGS

RUN pip install --no-cache-dir gunicorn==$GUNICORN_VERSION

COPY $REQUIREMENTS /app/
RUN pip install --no-cache-dir -r $REQUIREMENTS

COPY $SETTINGS /settings/dockerdeployer.py

COPY init_database.py /script/
COPY check_connection.py /script/
COPY create_django_admin_user.py /script/
COPY entrypoint.sh /script/

RUN ["chmod", "+x", "/script/entrypoint.sh"]
