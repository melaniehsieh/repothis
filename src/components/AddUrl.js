import React, { useState } from "react";
import "./styles.css";
import { VscTriangleUp } from "react-icons/vsc";

const AddUrl = () => {
  const [url, setUrl] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [output, setOutput] = useState([]);

  async function handleSubmit(e) {
    e.preventDefault();
    console.log(e.target.value);
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

      fetch("/nltkrepo", requestOptions)
        .then((res) => res.text().then((value) => setOutput(value)))
        .then((result) => console.log(result))
        .catch((error) => console.log("error", error));

      setTimeout(() => {
        setIsLoading(false);
      }, 1500);
    } catch (e) {
      console.log(e);
    }
  }

  console.log(output)
  return (
    <form className="add-url" onSubmit={handleSubmit}>
      <input
        id="url"
        type="url"
        placeholder="Enter Github Repository URL..."
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      <p>{output}</p>
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
    </form>
  );
};

export default AddUrl;
