FROM python:3.7

# build args
ARG BASE_DIR="/usr/src"
ARG APP_DIR="${BASE_DIR}app"
ARG APP_PORT=5000
ARG user=app
ARG group=app
ARG uid=1000
ARG gid=1000

#set work directory
WORKDIR "${APP_DIR}"

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PY_VENV_DIR "${BASE_DIR}/venv"
ENV WSGI_PORT "${APP_PORT}"


## install system dependencies
#RUN apt-get update && apt-get install -y --no-install-recommends gcc
#COPY ./packageInstallScript.sh ..
#RUN chmod 777 ../packageInstallScript.sh
#RUN .././packageInstallScript.sh

RUN pip install --upgrade pip && \
    pip install virtualenv

# setting python venv
RUN python -m venv ${PY_VENV_DIR}

COPY . "${APP_DIR}"
COPY ./requirements.txt .
RUN "${PY_VENV_DIR}/bin/pip" install -r requirements.txt


RUN groupadd -g ${gid} ${group} && useradd -u ${uid} -g ${group} -s /bin/sh ${user}

USER app


CMD ["/usr/src/venv/bin/gunicorn", "--bind", "0.0.0.0:80", "wsgi:app"]

