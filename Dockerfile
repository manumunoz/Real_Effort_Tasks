FROM python:3-alpine

ENV REDIS_URL="redis://redis:6379" \
    DJANGO_SETTINGS_MODULE="settings"

ADD ./ /opt/otree
ADD ./entrypoint.sh /entrypoint.sh
ADD ./pg_ping.py /pg_ping.py

RUN apk -U add --no-cache bash \
                          curl \
                          gcc \
                          musl-dev \
                          postgresql \
                          postgresql-dev \
                          libffi \
                          libffi-dev \
    && pip install --no-cache-dir -r /opt/otree/requirements.txt \
    && mkdir -p /opt/init \
    && chmod +x /entrypoint.sh \
    && apk del curl gcc musl-dev postgresql-dev libffi-dev

WORKDIR /opt/otree
VOLUME /opt/init
ENTRYPOINT ["/entrypoint.sh"]
CMD ["otree", "runprodserver", "--port=80"]
EXPOSE 80
