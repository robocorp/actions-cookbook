FROM debian:bookworm

# Set all variables that affect programs to follow same encoding
ENV LANG=C.UTF-8 LANGUAGE=C.UTF-8 LC_ALL=C.UTF-8

RUN apt-get update --fix-missing \
    && apt-get upgrade -y \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
        nginx \ 
        supervisor \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* 


COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

RUN useradd --no-log-init --system --create-home --shell /bin/bash worker

# Running as non sudo user 'worker'
USER worker
WORKDIR /home/worker

RUN mkdir -p /action-server
WORKDIR /action-server

# TODO: The Action Server version used need to be somehow visible here
# At the moment just printing.
RUN curl -o action-server https://downloads.robocorp.com/action-server/releases/latest/linux64/action-server \ 
    && chmod +x action-server \
    action-server version

#### Above this could be a base image in docker hub #### 
# We can do the base repo later.

# Copy the action folder(s)
# TODO: Something like: 'action-server export' that excludes files and folders 
# that are not needed/allowed in when running the action and push out a zip
COPY .\*.py .
COPY .\*.yaml .
COPY .\README.md .

# Coming soon:
# The command should build the env. and essentially prep anything that can be prepped into files
# This way the docker image will be as ready as possible in an immutable form
# RUN .\action-server prepare

EXPOSE 8080

CMD ["/usr/bin/supervisord"]