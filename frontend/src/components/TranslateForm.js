import React, { useState } from "react";
import axios from "axios";

function TranslateForm({ filename }) {
  const [lang, setLang] = useState("pl"); // Default: Polish
  const [translating, setTranslating] = useState(false);
  const [translatedFile, setTranslatedFile] = useState("");

  const handleTranslate = async () => {
    if (!filename) return alert("No file uploaded yet.");

    const formData = new FormData();
    formData.append("filename", filename);
    formData.append("lang", lang);

    try {
      setTranslating(true);
      const response = await axios.post("http://127.0.0.1:8000/translate", formData);
      setTranslatedFile(response.data.translated_file);
    } catch (error) {
      console.error(error);
      alert("Translation failed.");
    } finally {
      setTranslating(false);
    }
  };

  return (
    <div style={{ marginTop: "2rem" }}>
      <h2>Step 2: Translate your form</h2>
      <label>
        Target language:
        <select value={lang} onChange={(e) => setLang(e.target.value)}>
          <option value="pl">Polish</option>
          <option value="he">Hebrew</option>
          <option value="en">English</option>
          <option value="uk">Ukrainian</option>
          <option value="ru">Russian</option>
        </select>
      </label>
      <button onClick={handleTranslate} disabled={translating}>
        {translating ? "Translating..." : "Translate"}
      </button>

      {translatedFile && (
        <p style={{ marginTop: "1rem" }}>
          ✅ Translated file ready: <strong>{translatedFile}</strong>
        </p>
      )}
    </div>
  );
}

export default TranslateForm;
