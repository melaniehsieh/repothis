import React from "react";
import "./styles.css";

const ShowText = ({ output }) => {
  return (
    <div className="container">
      <p>{output}</p>
    </div>
  );
};

export default ShowText;
