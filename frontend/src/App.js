import React, { useState } from "react";
import "./App.css";

export default function App() {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [feedback, setFeedback] = useState(null);

  const uploadToBackend = (file) => {
    const formData = new FormData();
    formData.append("resume", file);
    formData.append("jobDesc", jobDescription);

    fetch("http://localhost:5001/analyze", {
      method: "POST",
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        setIsProcessing(false);
        setFeedback(data);
      })
      .catch(() => {
        alert("Backend error — is Flask running?");
        setIsProcessing(false);
      });
  };

  const handleFile = (e) => {
    const file = e.target.files[0];
    if (file) {
      setUploadedFile(file);
      setIsProcessing(false);
    }
  };

  const resetAll = () => {
    setUploadedFile(null);
    setJobDescription("");
    setFeedback(null);
  };

  return (
    <div className="App">
      <h1 className="title">AI Resume Screener</h1>

      <div className="container">

        <div className="card">
          <h2>Upload Resume</h2>

          {!uploadedFile ? (
            <label className="upload-box">
              <input type="file" accept=".pdf" onChange={handleFile} />
              Click to upload PDF
            </label>
          ) : (
            <div className="file-info">
              <strong>{uploadedFile.name}</strong>
              <small>{(uploadedFile.size / 1024 / 1024).toFixed(2)} MB</small>
            </div>
          )}

          <textarea
            className="jd-box"
            placeholder="Paste job description here (optional)..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          />

          <button
            className="analyze-btn"
            disabled={!uploadedFile}
            onClick={() => {
            setIsProcessing(true);
            uploadToBackend(uploadedFile);
            }}
            >
            Analyze Resume
          </button>


          {isProcessing && <p className="loading">Analyzing...</p>}
          {feedback && !isProcessing && (
            <p className="success">Analysis complete!</p>
          )}

          {uploadedFile && (
            <button className="reset" onClick={resetAll}>
              Upload New File
            </button>
          )}
        </div>


        <div className="card">
          <h2>AI Feedback</h2>

          {!feedback ? (
            <p className="placeholder">Upload a resume to get feedback.</p>
          ) : (
            <>
              <div className="score-box">
                <span>Overall Score</span>
                <h3>{feedback.overallScore}/100</h3>
                <div className="progress">
                  <div
                    className="progress-fill"
                   style={{ width: `${feedback.overallScore}%` }}
                  ></div>
                </div>
              </div>

              <p className="summary">{feedback.summary}</p>

              <h3>Categories</h3>
              {feedback.categories.map((c, i) => (
                <div key={i} className="category">
                  <div className="category-header">
                    <span>{c.title}</span>
                    <strong>{c.score}</strong>
                  </div>
                  {c.issues.map((issue, j) => (
                    <p key={j} className="issue">{issue.message}</p>
                  ))}
                </div>
              ))}

              <h3>Suggestions</h3>
              <ul>
                {feedback.suggestions.map((s, i) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
            </>
          )}
        </div>
      </div>
    </div>
  );
} 