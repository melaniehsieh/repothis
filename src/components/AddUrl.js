import React, { useState } from "react";
import "./styles.css";
import { VscTriangleUp } from "react-icons/vsc";

const AddUrl = () => {
  const [url, setUrl] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setIsLoading(true);
    console.log(e.target.value);
    try {
      setTimeout(() => {
        setIsLoading(false);
      }, 1500);
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
    </form>
  );
};

export default AddUrl;