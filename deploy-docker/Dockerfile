FROM debian:bookworm-slim

# Setup Nginx and Supervisor
RUN apt-get update && apt-get install -y nginx supervisor && \
    rm -rf /var/lib/apt/lists/*

COPY config/nginx.conf /etc/nginx/nginx.conf
COPY config/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Setup user and permissions
RUN useradd -m as-user
RUN chown -R as-user:as-user /tmp /var/log /run /var/lib/nginx

# Setup workspace
RUN mkdir -p /action-server /tmp/datadir
RUN chown -R as-user:as-user /action-server /tmp/datadir

WORKDIR /action-server

# Setup Action Server
ADD https://downloads.robocorp.com/action-server/releases/latest/linux64/action-server /usr/local/bin/action-server
RUN chmod +x /usr/local/bin/action-server

USER as-user

COPY . .
RUN action-server import --datadir=/tmp/datadir

EXPOSE 8080

CMD ["/usr/bin/supervisord"]