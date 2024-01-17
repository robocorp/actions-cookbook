from ubuntu:latest

RUN apt update && apt install python3 python3-pip -y && apt clean

RUN mkdir -p /action-server
WORKDIR /action-server

RUN pip install --upgrade robocorp-action-server
COPY . .

RUN apt-get update && apt-get install -y nginx supervisor && \
    rm -rf /var/lib/apt/lists/*

COPY ./docker/nginx.conf /etc/nginx/nginx.conf
COPY ./docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8080

CMD ["/usr/bin/supervisord"]