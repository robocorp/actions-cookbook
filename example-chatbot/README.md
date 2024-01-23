# ⚡️ Action Server chatbot

This is an example of [Robocorp Action Server](https://github.com/robocorp/robo/tree/master/action_server/docs#readme) working as an AI chatbot server for it's own actions.

## Before you start

The example uses the [Next.js OpenAI starter](https://github.com/vercel/ai/tree/main/examples/next-openai) for the browser based chat interface and you will need [Node.js](https://nodejs.org/en) installed to run it.

You will need an [OpenAI API key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-api-key) to get started quickly. Set it in the `.env` file:

```shell
OPENAI_API_KEY=XXXXXX
```

> [!TIP]
> Alternativelly, you can update `./actions-chat.py` to use a different model using a different [Langchain Agent](https://python.langchain.com/docs/modules/agents/agent_types/).

## Start the chatbot

First, start your Action Server as usual with `action-server start`

Parallelly, in the [./ui](./ui/) folder, install the chatbot UI dependencies and start the frontend server:

```sh
npm install
npm run dev
```

And your chatbot should be available at http://localhost:3000 🎉

> [!NOTE]
> Create a `./ui/.env` and define the `NEXT_PUBLIC_ACTION_SERVER_URL` value if your Action Server is running on a different port or you renamed the chat actions

---

### Next steps

- 🦜 Follow the [Langchain documentation](https://python.langchain.com/docs/get_started/introduction) for further configuration of the AI agent
- 🦜 See the [Vercel AI SDK](https://sdk.vercel.ai/docs) for the documentation of the frontend UI
- 🌟 Check out other [Action Server examples](https://github.com/robocorp/actions-cookbook) for reference and inspiration
- 🙋‍♂️ Look for further assistance and help in the main [Robocorp repo](https://github.com/robocorp/robocorp)
