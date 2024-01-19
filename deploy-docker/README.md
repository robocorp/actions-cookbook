# Run ⚡️Action Server with Docker

This an example on how to build and run [Robocorp Action Server](https://github.com/robocorp/robo/tree/master/action_server/docs#readme) with [Docker](https://www.docker.com/)

This example assumes you have your actions already created, tested and ready to launch. The example also uses minimal configuration as a starting point for your own custom setup.

## Install Docker

To run Docker images locally, first install the [Docker Engine](https://docs.docker.com/engine/install/) on your machine.

## Prepare your Action Server

This setup will the [Dockerfile](./Dockerfile) to setup Action Server in tandem with [Nginx](https://www.nginx.com) as a proxy server and utilize [Supervisor](https://supervisord.org/) for process control.

Setting up configuration file for each is needed - you can leave them as in this example or update to your needs:

- Docker [./Dockerfile](./docker/Dockerfile) to setup the base Python image
- Nginx [./docker/nginx.conf](./docker/nginx.conf) to expose endpoints needed for use in AI applications
- Supervisor [./docker/supervisord.conf](./docker/supervisord.conf) to handle the service management

## Build and Run

Once everything is setup, build your Docker image:

```sh
docker build -t my-action-server-app .
```

> [!NOTE]
> If you are on a Mac wiht Apple silicon, don't forget to add the correct platform flag:
>
> `docker build -t my-action-server-app . --platform linux/amd64`

And once the build is done, run it:

```sh
docker run -p 3000:8080 -p 4000:8087 my-action-server-app
```

Your Action Server now exposes two endpoints:

- ⚡️ http://localhost:4000 - Your Action Server Control Panel
- 🌍 http://localhost:3000 - Action Server API ready to be used in local AI applications

> [!WARNING]
> In this example Action Server is running without a set API key or external url defined – how to configure these depends on your deployment environment or chose provider – see other [Action Server deploy examples](https://github.com/robocorp/actions-cookbook) for reference on how to do it.

---

### Next steps

- 🌟 Check out other [Action Server examples](https://github.com/robocorp/actions-cookbook) for reference and inspiration
- 🙋‍♂️ Look for further assistance and help in the main [Robocorp repo](https://github.com/robocorp/robocorp)
