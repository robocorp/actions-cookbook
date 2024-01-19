ARG PYTHON_VERSION=3.11

FROM python:${PYTHON_VERSION}

RUN apt-get update && apt-get install -y

RUN mkdir -p /action-server
WORKDIR /action-server

RUN pip install --upgrade robocorp-action-server
COPY . .

RUN apt-get update && apt-get install -y nginx supervisor && \
    rm -rf /var/lib/apt/lists/*

COPY config/nginx.conf /etc/nginx/nginx.conf
COPY config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8080

CMD ["/usr/bin/supervisord"]