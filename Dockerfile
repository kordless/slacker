FROM alpine:3.5

RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
  && pip install slacker \
  && rm -rf /var/cache/apk/*

WORKDIR /app
COPY main.py /app/
COPY requirements.txt /app/

ONBUILD RUN virtualenv /env && /env/bin/pip install -r /app/requirements.txt

ADD static /app/static/

EXPOSE 8080
CMD ["/usr/bin/python", "main.py"]
