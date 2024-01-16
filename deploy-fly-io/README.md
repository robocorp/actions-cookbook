# Deploy ⚡️ Action Server to fly.io

This an example on how to deploy your [Robocorp Action Server](https://github.com/robocorp/robo/tree/master/action_server/docs#readme) to [fly.io](fly.io).

This example assumes you have your actions already created, tested and ready to launch. The example also uses minimal configuration as a starting point for your own custom setup.

## Setup fly.io

Follow the [fly.io Speedrun](https://fly.io/docs/speedrun/) on how to setup your account. You will need to [install the flyctl](https://fly.io/docs/hands-on/install-flyctl/) command-line utility and setup an account via it.

## Prepare your Action Server

THe deployment will utilize a [./docker/Dockerfile](./docker/Dockerfile) that will setup a Python based image to install and run Action Server itself, use [Nginx](https://www.nginx.com) as a proxy and [Supervisor](https://supervisord.org/) for process control. You can leave the file as is or update it to your likings and needs:

```Dockerfile
ARG PYTHON_VERSION=3.11

FROM python:${PYTHON_VERSION}

RUN apt-get update && apt-get install -y

RUN mkdir -p /action-server
WORKDIR /action-server

# Install and setup Action Server
RUN pip install robocorp-action-server
COPY . .

# Install and setup Nginx and Supervisor
RUN apt-get update && apt-get install -y nginx supervisor && \
    rm -rf /var/lib/apt/lists/*

COPY docker/nginx.conf /etc/nginx/nginx.conf
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8080

CMD ["/usr/bin/supervisord"]
```

Nginx will use the [./docker/nginx.conf](./docker/nginx.conf) config file to setup a proxy and expose only those Action Server endpoints that are required for AI applications.

```nginx
events {}

http {
    include       mime.types;
    charset       utf-8;

    server {
        listen 0.0.0.0:8080;

        location = / {
            proxy_pass http://localhost:8087/openapi.json;
        }

        location /openapi.json {
            proxy_pass http://localhost:8087/openapi.json;
        }

        location /api/ {
            proxy_pass http://localhost:8087;
        }
    }
}
```

Supervisor [./docker/supervisord.conf](./docker/supervisord.conf) will handle launching both Action Server and Nginx in tandem and report the logs to fly.io:

```ini
[supervisord]
nodaemon=true

[program:nginx]
command=/usr/sbin/nginx -g "daemon off;"
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0

[program:action-server]
command=action-server start --server-name=%(ENV_FLY_APP_NAME)sfly.dev --api-key=%(ENV_ACTION_SERVER_KEY)s --port 8087
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0
```
---

As the final configuration, a fly.io configuration file [./fly.toml](./fly.toml) is needed.

Adjust the `app` value to match your application name:

```toml
app = "action-server-fly-io-example"

[build]
  dockerfile = "docker/Dockerfile"

[http_service]
  internal_port = 8080
  force_https = true
```

## Set your API key

To protect your actions, setup an API key for Action Server – [the fly.io secrets](https://fly.io/docs/reference/secrets/) feature is perfect for this:

```sh
fly secrets set ACTION_SERVER_KEY=your-secret-key
```

> [!NOTE]
> Remember and do not share the API key as you will need it when setting up your AI application

## Deploy

Once everything is setup, run `fly launch` and follow the instructions 🚀

If everything goes well 🤞 you will end up with a url like https://action-server-fly-io-example.fly.dev that is ready to be used in OpenAI GPTs and other AI applications.

---

### Next steps

- 📖 Follow the [fly.io documentation](https://fly.io/docs/) for next steps and further configuration of the deployment
- 🌟 Check out other [Action Server examples](https://github.com/robocorp/actions-cookbook) for references and inspiration
- 🙋‍♂️ Look for further help in the main[Robocorp repo](https://github.com/robocorp/robocorp)
