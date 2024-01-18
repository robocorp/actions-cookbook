# Deploy ⚡️Action Server to Render

This an example on how to deploy your [Robocorp Action Server](https://github.com/robocorp/robo/tree/master/action_server/docs#readme) to [Render](https://render.com).

This example assumes you have your actions already created, tested and ready to launch. The example also uses minimal configuration as a starting point for your own custom setup.

## Setup Render

You will need to create an account [Render.com](https://render.com). Easiest way to get started is by deploying your Action Server from a Git repository, so no additional setup is needed.

## Prepare your Action Server

The deployment will use [Render Docker deployment](https://docs.render.com/docker) and will setup [Nginx](https://www.nginx.com) as a proxy server and utilize [Supervisor](https://supervisord.org/) for process control.

Setting up configuration file for each is needed - you can leave them as in this example or update to your needs:

- Docker [./docker/Dockerfile](./docker/Dockerfile) to setup the base Python image
- Nginx [./docker/nginx.conf](./docker/nginx.conf) to expose endpoints needed for use in AI applications
- Supervisor [./docker/supervisord.conf](./docker/supervisord.conf) to handle the service management

---

As the final step – create the Render configuration file [./render.yaml](./render.yaml).

Adjust the `name` value to match your application name and the `repo` URL:

```yaml
services:
  - type: web
    name: action-server-render-example
    env: docker
    repo: https://github.com/your-username/your-repository
    dockerfilePath: ./docker/Dockerfile
    dockerContext: .
    envVars:
      - key: ACTION_SERVER_KEY
        sync: false
```

## Deploy

Once everything is setup, commit your changes and in Render dashboard create a new [Web service](https://docs.render.com/web-services) and connect it to your Action Server repository.

Follow the instructions and don't forget to setup the `ACTION_SERVER_KEY` Environment Variable with a secure private key for the Action Server use.

> [!NOTE]
> Protect and remember the API key – you will need it when setting up your AI application

If everything goes well 🤞 you will end up with an url like https://action-server-example.onrender.com/ that is ready to be used in OpenAI GPTs and other AI applications.

---

### Next steps

- 📖 Follow the [Render documentation](https://docs.render.com/) for further configuration of the deployment infrastructure
- 🌟 Check out other [Action Server examples](https://github.com/robocorp/actions-cookbook) for reference and inspiration
- 🙋‍♂️ Look for further assistance and help in the main [Robocorp repo](https://github.com/robocorp/robocorp)
