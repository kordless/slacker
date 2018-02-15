FROM alpine:3.5

RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
    sqlite3 \
  && pip install slacker \
  && pip install tweepy \
  && pip install pysqlite \
  && pip install requests \
  && rm -rf /var/cache/apk/*

WORKDIR /app
COPY main.py /app/

ADD static /app/static/

CMD ["/usr/bin/python", "main.py"]
