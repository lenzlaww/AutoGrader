import React, { useState } from "react";
import FileUpload from "./components/FileUpload";
import ResultDisplay from "./components/ResultDisplay";
import "./styles.css";

function App() {
  const [results, setResults] = useState(null);
  return (
    <div className="App">
      <h1>AutoGrader</h1>
      <p>AI-Powered Teacher Assistant</p>
      <FileUpload setResults={setResults} />
      <ResultDisplay results={results} />
    </div>
  );
}
export default App;