# FROM mtr.devops.telekom.de/mcsps/python:3-slim
# LABEL org.opencontainers.image.authors="mcs-dis@telekom.de"
# LABEL version="1.0.0"
# LABEL description="Alertmanager Webhook Webex Teams"
FROM python:3.9-slim

# ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install ca-certificates -y && update-ca-certificates

COPY webex/webex.py /home/appuser/webex.py
COPY webex/wsgi.py /home/appuser/wsgi.py
COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt
RUN useradd --create-home appuser
WORKDIR /home/appuser
USER root
ENV PYTHONUNBUFFERED=0
ENV WEBHOOKPORT=9091
ENTRYPOINT gunicorn --bind 0.0.0.0:${WEBHOOKPORT} --access-logfile /dev/stdout wsgi:app
