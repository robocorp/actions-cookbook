FROM debian:bookworm-slim

# Setup Nginx and Supervisor
RUN apt-get update && apt-get install -y nginx supervisor && \
    rm -rf /var/lib/apt/lists/*

COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Setup user and permissions
RUN useradd -m as-user
RUN chown -R as-user:as-user /var/log /run /var/lib/nginx

# Setup workspace
RUN mkdir -p /action-server/datadir /action-server/actions
RUN chown -R as-user:as-user /action-server

WORKDIR /action-server/actions

# Setup Action Server
ADD https://downloads.robocorp.com/action-server/releases/latest/linux64/action-server /usr/local/bin/action-server
RUN chmod +x /usr/local/bin/action-server

USER as-user

COPY . .
RUN action-server import --datadir=/action-server/datadir

EXPOSE 8080

CMD ["/usr/bin/supervisord"]