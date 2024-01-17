# Deploy ⚡️Action Server to Digital Ocean

This an example on how to deploy your [Robocorp Action Server](https://github.com/robocorp/robo/tree/master/action_server/docs#readme) to [Digital Ocean](https://www.digitalocean.com).

This example assumes you have your actions already created, tested and ready to launch. The example also uses minimal configuration as a starting point for your own custom setup.

## Setup Digital Ocean

You will need to setup an account with Digital Ocean and optinally [install the doctl](https://docs.digitalocean.com/reference/doctl/how-to/install/) command-line utility.

## Prepare your Action Server

The deployment will use a [Docker deployment](https://docs.digitalocean.com/products/app-platform/how-to/deploy-from-container-images/) and will setup [Nginx](https://www.nginx.com) as a proxy server and utilize [Supervisor](https://supervisord.org/) for process control.

Setting up configuration file for each is needed - you can leave them as in this example or update to your needs:

- Docker [./docker/Dockerfile](./docker/Dockerfile) to setup the base Python image
- Nginx [./docker/nginx.conf](./docker/nginx.conf) to expose endpoints needed for use in AI applications
- Supervisor [./docker/supervisord.conf](./docker/supervisord.conf) to handle the service management

---

As the final step – create the Digital Ocean configuration file [./.do/app.yaml](./.do/app.yaml).

Adjust the `name` to match your application name and update the `git` and `source_dir` values:

```yaml
name: action-server-do-example

services:
  - name: action-server
    dockerfile_path: ./docker/Dockerfile
    git:
      branch: main
      repo_clone_url: https://github.com/your-username/your-repository.git
    routes:
      - path: /
```

## Deploy

You can now use the [Digital Ocean App Platform Quickstart](https://docs.digitalocean.com/products/app-platform/getting-started/quickstart/) to connect your repository to Digital Ocean.

Optionally, you can also deploy the Application via cli:

```sh
doctl apps create --spec .do/app.yaml
```

If everything goes well 🤞 your application will get built and deployed. 🚀

## Set your API key and URL

To finish the application setup, you will need to [create two Environment Variables](https://docs.digitalocean.com/products/app-platform/how-to/use-environment-variables/#using-bindable-variables-within-environment-variables) inside your freshly created Application:

- `ACTION_SERVER_URL` - the Live App URL of your application
- `ACTION_SERVER_API` - an API key for Action Server, you should `Encrypt` this variable

> [!NOTE]
> Protect and remember the API key – you will need it when setting up your AI application

---

### Next steps

- 📖 Follow the [Digital OCean documentation](https://docs.digitalocean.com) for further configuration of the deployment infrastructure
- 🌟 Check out other [Action Server examples](https://github.com/robocorp/actions-cookbook) for reference and inspiration
- 🙋‍♂️ Look for further assistance and help in the main [Robocorp repo](https://github.com/robocorp/robocorp)
