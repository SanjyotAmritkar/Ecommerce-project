import React, { useState } from "react";

function Chatbot() {
  const [input, setInput] = useState("");
  const [chat, setChat] = useState([]);

  const sendMessage = async () => {
    const res = await fetch("http://localhost:8000/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: input })
    });

    const data = await res.json();
    setChat([...chat, { user: input, bot: data.response }]);
    setInput("");
  };

  return (
    <div>
      <h2>Amazon Product Chatbot</h2>
      <div>
        {chat.map((msg, idx) => (
          <div key={idx}>
            <b>You:</b> {msg.user}
            <br />
            <b>Bot:</b> {msg.bot}
            <hr />
          </div>
        ))}
      </div>
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}

export default Chatbot;
