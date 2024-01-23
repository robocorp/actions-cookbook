"use client";
import { useEffect, useState } from "react";
import { useChat } from "ai/react";

const actionServerEndpoint =
  process.env.NEXT_PUBLIC_ACTION_SERVER_URL ||
  "http://localhost:8080/api/actions/example-chatbot/chat-completion/run";

export default function Chat() {
  const [messageBlob, setMessageBlob] = useState<string>("");

  const { messages, input, handleInputChange, handleSubmit } = useChat({
    api: actionServerEndpoint,
    body: {
      messages: messageBlob,
    },
  });

  useEffect(() => {
    setMessageBlob(JSON.stringify({ input, messages: messages }));
  }, [input, messages]);

  return (
    <div className="flex flex-col w-full max-w-md py-24 mx-auto stretch">
      {messages.map((m) => (
        <div key={m.id} className="whitespace-pre-wrap mb-4">
          <strong>{m.role === "user" ? "User: " : "AI: "}</strong>
          {m.content}
        </div>
      ))}

      <form onSubmit={handleSubmit}>
        <input
          className="fixed bottom-0 w-full max-w-md p-2 mb-8 border border-gray-300 rounded shadow-xl"
          value={input}
          placeholder="Say something..."
          onChange={handleInputChange}
        />
      </form>
    </div>
  );
}
