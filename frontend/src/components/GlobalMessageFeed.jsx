import React, { useEffect, useState, useContext } from "react";
import io from "socket.io-client";
import { AuthCtx } from "../context/AuthContext";
import DOMPurify from "dompurify";

const ws = io(import.meta.env.VITE_API_URL.replace("/api", "/ws"), { autoConnect: true });

export default function GlobalMessageFeed() {
  const { jwt } = useContext(AuthCtx);
  const [messages, setMessages] = useState([]);
  const [inputVal, setInputVal] = useState("");
  const [globalViewers, setGlobalViewers] = useState(0);

  useEffect(() => {
    fetch(import.meta.env.VITE_API_URL + "/messages?limit=50")
      .then(res => res.json())
      .then(data => setMessages(data));

    ws.on("message_new", newMsg => {
      setMessages(prev => [...prev, newMsg]);
    });
    ws.on("global_viewers", count => setGlobalViewers(count));

    return () => {
      ws.off("message_new");
      ws.off("global_viewers");
    };
  }, []);

  const handleSend = async () => {
    if (!inputVal.trim()) return;
    const res = await fetch(`${import.meta.env.VITE_API_URL}/messages`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: jwt ? `Bearer ${jwt}` : "",
      },
      body: JSON.stringify({ content: inputVal }),
    });
    if (res.ok) setInputVal("");
    else alert("Failed to send message. Are you logged in?");
  };

  return (
    <div className="border p-4 rounded">
      <h2 className="text-lg font-bold mb-2">Global Message Feed</h2>
      <div className="mb-2 text-sm text-gray-500">
        Live viewers: {globalViewers}
      </div>
      <div className="max-h-64 overflow-y-auto bg-gray-100 p-2 rounded mb-2">
        {messages.map(m => (
          <div key={m.id} className="mb-1">
            <span className="font-semibold mr-1">
              {m.author_id ? `User#${m.author_id}` : "Guest"}:
            </span>
            {/* Replace plain text with sanitized render */}
            <span dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(m.content) }} />
          </div>
        ))}
      </div>
      <div className="flex items-center">
        <input
          type="text"
          className="flex-1 border rounded px-2"
          placeholder="Say something..."
          value={inputVal}
          onChange={e => setInputVal(e.target.value)}
          disabled={!jwt}
        />
        <button onClick={handleSend} className="btn ml-2" disabled={!jwt}>
          Send
        </button>
      </div>
      {!jwt && (
        <div className="text-xs text-red-500 mt-1">
          Please log in to post a message.
        </div>
      )}
    </div>
  );
}
