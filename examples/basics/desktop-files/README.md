# Connect your local compute's folder to ChatGPT

Instead of drag and dropping files to ChatGPT for additional context, what if you could just keep the files on your local folder, and let ChatGPT access them when needed? Pretty wild, right? But that's exactly what this action does!

> [!WARNING]  
> Be careful with this action, as you essentially expose a part of your own computer to the public internet. This is made for demonstrating the power of Python actions when used with ChatGPT, not for production usage.

So this example shows how to securely expose files from your local folder to an LLM, using Action Server. To set things up, you'll need to create a folder locally on your machine (or available for the Action Server runs), and update it's name to the code.

The demo only supports `.txt` and `.pdf` files, and for PDFs only the first page is extracted. PDFs need to be text-based, not images. You are welcome to open a PR and improve the file reading! 👩‍💻

Remember to update the folder name in the code!

```py
path = "/Users/tommi/Desktop/available_to_ai/"
```