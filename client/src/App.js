// import { useState } from 'react';
// import axios from 'axios';
// import { Input, Textarea } from '@nextui-org/react';
// import styles from './App.css';

// export default function App() {
//   const [question, setQuestion] = useState('');
//   const [response, setResponse] = useState('');

//   const handleSubmit = async (e) => {
//     e.preventDefault();

//     try {
//       const res = await axios.post('/api/query', { question });
//       setResponse(res.data.response);
//     } catch (error) {
//       console.error(error);
//       setResponse('Error occurred. Please try again.');
//     }
//   };

//   return (
//     <div className="container">
//       <div className="textContainer">
//         <h1 className="title">Welcome to ChatUTD</h1>
//       </div>
//       <form onSubmit={handleSubmit} className="form">
//       <Textarea
//       label="Ask ChatUTD a quedtion!"
//       placeholder="Enter your amazing ideas."
//       onChange={(e) => setQuestion(e.target.value)}
//     />

//         {/* <Input
//           placeholder="Ask a question"
//           value={question}
//           onChange={(e) => setQuestion(e.target.value)}
//         /> */}
//         <button type="submit">Submit</button>
//       </form>
//       {response && <p className="response">{response}</p>}
//     </div>
//   );
// }

//BELOW IS THE FETCH API VERSION

// import { useState, useEffect } from "react";
// import "./App.css";
// import lens from "./assets/lens.png";
// import loadingGif from "./assets/loading.gif";

// function App() {
//   const [prompt, updatePrompt] = useState(undefined);
//   const [loading, setLoading] = useState(false);
//   const [answer, setAnswer] = useState(undefined);

//   useEffect(() => {
//     if (prompt != null && prompt.trim() === "") {
//       setAnswer(undefined);
//     }
//   }, [prompt]);

//   const sendPrompt = async (event) => {
//     if (event.key !== "Enter") {
//       return;
//     }

//     try {
//       setLoading(true);

//       const requestOptions = {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ prompt }),
//       };

//       const res = await fetch("/api/ask", requestOptions);

//       if (!res.ok) {
//         throw new Error("Something went wrong");
//       }

//       const { message } = await res.json();
//       setAnswer(message);
//     } catch (err) {
//       console.error(err, "err");
//     } finally {
//       setLoading(false);
//     }
//   };

//   return (
//     <div className="app">
//       <div className="app-container">
//       <h1 className="title">Welcome to ChatUTD</h1>
//         <div className="spotlight__wrapper">
//           <input
//             type="text"
//             className="spotlight__input"
//             placeholder="Ask me anything..."
//             disabled={loading}
//             style={{
//               backgroundImage: loading ? `url(${loadingGif})` : `url(${lens})`,
//             }}
//             onChange={(e) => updatePrompt(e.target.value)}
//             onKeyDown={(e) => sendPrompt(e)}
//           />
//           <div className="spotlight__answer">{answer && <p>{answer}</p>}</div>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default App;


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
        <h1 className="title">Welcome to ChatUTD</h1>
        <div className="spotlight__wrapper">
          <input
            type="text"
            className="spotlight__input"
            placeholder="Ask me anything..."
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
