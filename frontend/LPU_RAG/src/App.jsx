import { useState } from "react";
import axios from "axios";

function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    if (!query.trim()) return;

    const userMessage = { type: "user", text: query };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const res = await axios.post("https://lpu-rag-backend.onrender.com/ask", {
        query: query,
      });
      setQuery("")

      const botMessage = {
        type: "bot",
        text: res.data.answer,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { type: "bot", text: "Error connecting to server" },
      ]);
    }

    setQuery("");
  };

  return (
    <div className="h-screen flex flex-col bg-gray-100">
      
      {/* Header */}
      <div className="bg-blue-600 text-white p-4 text-lg font-semibold">
        LPU RAG Chatbot
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`max-w-xl px-4 py-2 rounded-lg ${
              msg.type === "user"
                ? "bg-blue-500 text-white ml-auto"
                : "bg-white text-gray-800 mr-auto shadow"
            }`}
          >
            {msg.text}
          </div>
        ))}
      </div>

      {/* Input Bar */}
      <div className="p-4 bg-white flex gap-2 border-t">
        <input
          type="text"
          placeholder="Ask something about LPU..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          className="flex-1 border rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <button
          onClick={sendMessage}
          className="bg-blue-600 text-white px-5 py-2 rounded-lg hover:bg-blue-700"
        >
          Send
        </button>
      </div>

    </div>
  );
}

export default App;