import React, { useState } from "react";
import "./styles.css";
import { VscTriangleUp } from "react-icons/vsc";
import ShowText from "./ShowText";

const AddUrl = () => {
  const [url, setUrl] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [output, setOutput] = useState([]);

  async function handleSubmit(e) {
    e.preventDefault();
    setIsLoading(true);
    try {
      let myHeaders = new Headers();
      myHeaders.append("Content-Type", "application/json");

      let raw = JSON.stringify({ repoUrl: url });

      let requestOptions = {
        method: "POST",
        headers: myHeaders,
        body: raw,
        redirect: "follow",
      };

      fetch("/repo", requestOptions)
        .then((response) => response.text())
        .then((result) => {
          setTimeout(() => {
            setIsLoading(false);
            setOutput(result.split(', '));
          }, 1500);
        })
        .catch((error) => console.log("error", error));
    } catch (e) {
      console.log(e);
    }
  }

  return (
    <form className="add-url" onSubmit={handleSubmit}>
      <input
        id="url"
        type="url"
        placeholder="Enter Github Repository URL..."
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      <button>
        {isLoading ? (
          <div>
            <VscTriangleUp className="spinner" />
            <span>Generating...</span>
          </div>
        ) : (
          <span>Generate</span>
        )}
      </button>
      <ShowText output={output} />
    </form>
  );
};

export default AddUrl;
