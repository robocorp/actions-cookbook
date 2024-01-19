# Deploy ⚡️Action Server to Railway

This an example on how to deploy your [Robocorp Action Server](https://github.com/robocorp/robo/tree/master/action_server/docs#readme) to [Railway.app](https://railway.app).

This example assumes you have your actions already created, tested and ready to launch. The example also uses minimal configuration as a starting point for your own custom setup.

## Setup Railway

You will need to create a [Railway.app](https://railway.app) account. Easiest way to get started is by creating a new Service connected to your Github account, so no additional setup is needed.

## Prepare your Action Server

The deployment will use [Railway Docker deployment](https://docs.railway.app/guides/dockerfiles) and will setup [Nginx](https://www.nginx.com) as a proxy server and utilize [Supervisor](https://supervisord.org/) for process control.

Setting up configuration file for each is needed - you can leave them as in this example or update to your needs:

- Docker [./docker/Dockerfile](./docker/Dockerfile) to setup the base Python image
- Nginx [./docker/nginx.conf](./docker/nginx.conf) to expose endpoints needed for use in AI applications
- Supervisor [./docker/supervisord.conf](./docker/supervisord.conf) to handle the service management

---

As the final step – create the Railway configuration file [./railway.toml](./railway.toml).

```toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "./deploy-railway/docker/Dockerfile"
```

## Deploy

Once everything is setup, commit your changes and in Render dashboard create a new [Service](https://docs.railway.app/overview/the-basics#services) and connect it to your Action Server Github repository.

Follow the instructions and don't forget to setup the `ACTION_SERVER_KEY` Environment Variable with a secure private key for the Action Server use.

> [!NOTE]
> Protect and remember the API key – you will need it when setting up your AI application

If everything goes well 🤞 you will end up with an url like https://action-server-example.onrender.com/ that is ready to be used in OpenAI GPTs and other AI applications.

---

### Next steps

- 📖 Follow the [fly.io documentation](https://fly.io/docs/) for further configuration of the deployment infrastructure
- 🌟 Check out other [Action Server examples](https://github.com/robocorp/actions-cookbook) for reference and inspiration
- 🙋‍♂️ Look for further assistance and help in the main [Robocorp repo](https://github.com/robocorp/robocorp)
