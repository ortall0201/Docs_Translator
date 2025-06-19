import React, { useState } from "react";
import axios from "axios";

function UploadForm({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleUpload = async () => {
    if (!file) return alert("Please select a file first.");
    const formData = new FormData();
    formData.append("file", file);

    try {
      setUploading(true);
      const response = await axios.post("http://127.0.0.1:8000/upload", formData);
      alert("Upload successful!");
      onUploadSuccess(response.data.filename);
    } catch (err) {
      console.error(err);
      alert("Upload failed.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <h2>Step 1: Upload your form</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={uploading}>
        {uploading ? "Uploading..." : "Upload"}
      </button>
    </div>
  );
}

export default UploadForm;
