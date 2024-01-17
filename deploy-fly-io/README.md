# Deploy ⚡️Action Server to fly.io

This an example on how to deploy your [Robocorp Action Server](https://github.com/robocorp/robo/tree/master/action_server/docs#readme) to [fly.io](fly.io).

This example assumes you have your actions already created, tested and ready to launch. The example also uses minimal configuration as a starting point for your own custom setup.

## Setup fly.io

Follow the [fly.io Speedrun](https://fly.io/docs/speedrun/) on how to setup your account. You will need to [install the flyctl](https://fly.io/docs/hands-on/install-flyctl/) command-line utility and setup an account via it.

## Prepare your Action Server

The deployment will use [fly.io Docker deployment](https://fly.io/docs/languages-and-frameworks/dockerfile/) and will setup [Nginx](https://www.nginx.com) as a proxy server and utilize [Supervisor](https://supervisord.org/) for process control.

Setting up configuration file for each is needed - you can leave them as in this example or update to your needs:

- Docker [./docker/Dockerfile](./docker/Dockerfile) to setup the base Python image
- Nginx [./docker/nginx.conf](./docker/nginx.conf) to expose endpoints need for AI application
- Supervisor [./docker/supervisord.conf](./docker/supervisord.conf) to handle launching the applications

---

As the final step – create the fly.io configuration file [./fly.toml](./fly.toml).

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
> Protect and remember the API key – you will need it when setting up your AI application

## Deploy

Once everything is setup, run `fly launch` and follow the instructions 🚀

If everything goes well 🤞 you will end up with an url like https://action-server-fly-io-example.fly.dev that is ready to be used in OpenAI GPTs and other AI applications.

---

### Next steps

- 📖 Follow the [fly.io documentation](https://fly.io/docs/) for further configuration of the deployment infrastructure
- 🌟 Check out other [Action Server examples](https://github.com/robocorp/actions-cookbook) for reference and inspiration
- 🙋‍♂️ Look for further assistance and help in the main [Robocorp repo](https://github.com/robocorp/robocorp)
