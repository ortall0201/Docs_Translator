import React, { useState } from "react";
import UploadForm from "./components/UploadForm";
import TranslateForm from "./components/TranslateForm";
import "./App.css";

function App() {
  const [filename, setFilename] = useState("");
  const [translatedFile, setTranslatedFile] = useState("");

  return (
    <div className="App">
      <header className="App-header">
        <h1>📄 Docs Translator</h1>

        {/* Step 1: Upload */}
        <UploadForm onUploadSuccess={setFilename} />

        {/* Step 2: Translate */}
        {filename && (
          <TranslateForm filename={filename} onTranslateSuccess={setTranslatedFile} />
        )}

        {/* Download link after translation */}
        {translatedFile && (
          <p>
            ✅ Translated file ready:{" "}
            <a
              href={`http://localhost:8000/download/${translatedFile}`}
              target="_blank"
              rel="noopener noreferrer"
              style={{ color: "#00ffcc", textDecoration: "underline" }}
            >
              {translatedFile}
            </a>
          </p>
        )}
      </header>
    </div>
  );
}

export default App;
