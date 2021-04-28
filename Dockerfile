FROM python:3.7-slim-buster

# build args
ARG APP_DIR="/usr/src/app"
ARG PY_VENV_DIR="${APP_DIR}/venv"

#set work directory
WORKDIR "${APP_DIR}"

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ARG user=app
ARG group=app
ARG uid=1000
ARG gid=1000

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
RUN "${PY_VENV_DIR}/bin/pip" install pip --upgrade
RUN "${PY_VENV_DIR}/bin/pip" install wheel
RUN "${PY_VENV_DIR}/bin/pip" install -r requirements.txt


RUN groupadd -g ${gid} ${group} && useradd -u ${uid} -g ${group} -s /bin/sh ${user}

USER app

CMD ["${PY_VENV_DIR}/bin/gunicorn", "--bind", "0.0.0.0:${WSGI_PORT}", "wsgi:app"]

