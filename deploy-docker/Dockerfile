FROM debian:bookworm-slim

# Setup Nginx and Supervisor
RUN apt-get update && apt-get install -y nginx supervisor && \
    rm -rf /var/lib/apt/lists/*

COPY config/nginx.conf /etc/nginx/nginx.conf
COPY config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Setup Action Server
RUN mkdir -p /action-server
WORKDIR /action-server

ADD https://downloads.robocorp.com/action-server/releases/latest/linux64/action-server /usr/local/bin/action-server
RUN chmod +x /usr/local/bin/action-server

COPY . .

RUN action-server import

EXPOSE 8080

CMD ["/usr/bin/supervisord"]