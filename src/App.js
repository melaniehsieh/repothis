import React from "react";
import "./App.css";
import AddUrl from "./components/AddUrl";

function App() {
  return (
    <div className="box">
      <h1>repothis</h1>
      <h3>Summarize Github documentations into 5 bullet points</h3>
      <AddUrl />
    </div>
  );
}

export default App;

// npm start
// cd api > venv\Scripts\activate > flask run --no-debugger
