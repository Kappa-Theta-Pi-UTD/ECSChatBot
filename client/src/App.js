

//BELOW IS THE AXIOS VERSION

import React, { useState, useEffect } from "react";
import api from "./api";
import axios from "axios";
import "./App.css";
import lens from "./assets/lens.png";
import loadingGif from "./assets/loading.gif";

function App() {
  const [prompt, updatePrompt] = useState(undefined);
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState(undefined);

  useEffect(() => {
    if (prompt != null && prompt.trim() === "") {
      setAnswer(undefined);
    }
  }, [prompt]);

  const sendPrompt = async (event) => {
    try {
      setLoading(true);

      const response = await api.post("/query", { question: prompt });

      const { response: answer } = response.data;
      setAnswer(answer);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === "Enter") {
      sendPrompt();
    }
  };


  return (
    <div className="app">
      <div className="app-container">
        <h1 className="title">ChatKTP</h1>
        <div className="spotlight__wrapper">
          <input
            type="text"
            className="spotlight__input"
            placeholder="Ask me anything about Institute for Innovation and Entrepreneurship..."
            disabled={loading}
            style={{
              backgroundImage: loading ? `url(${loadingGif})` : `url(${lens})`,
            }}
            value={prompt}
            onChange={(e) => updatePrompt(e.target.value)}
            onKeyDown={handleKeyPress}
          />
          <button
            className="spotlight__button"
            disabled={loading}
            onClick={sendPrompt}
          >
            Submit
          </button>
        </div>
        <div className="spotlight__answer">{answer && <p>{answer}</p>}</div>
      </div>
    </div>
  );
}

export default App;
