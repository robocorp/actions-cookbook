# Use Claude 3 to validate other LLMs answers

This is a fun example of an action that uses another LLM to validate the answers of the "primary" LLM and suggest for improvements. The idea is based out of a "what if" discussion in the community.

Also see a 📼 [**Youtube live coding video**](https://youtu.be/eSjAwIbkfEY) 📼 on how to use this with OpenAI Custom GPTs.

The code itself is really simple. Start by renaming `.env_example` to `.env`, and add your Anthropic API key there.

Action itself takes the user question and the proposed answer as inputs, and returns text that contains Claude's suggested improvements.

When adding Actions to e.g. Custom GPT, remember to add something along these lines to the instructions:

_"You are a helpful assistant that validates your own responses with an action before replying to the user. Use the action validate to do this. After receiving proposed changes, alter your final response to the user based on those suggestions, while still observing the original requirements and instructions from the user."_

Feedback and improvements welcome! 💪