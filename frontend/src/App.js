import React, { useState } from "react";
import "./App.css";

function App() {
  const [errorMessage, setErrorMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handlePredict = async () => {
    if (!errorMessage.trim()) {
      setError("Please enter an error message");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ error_message: errorMessage })
      });

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError("Server not reachable. Is backend running?");
    }

    setLoading(false);
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case "High":
        return "red";
      case "Medium":
        return "orange";
      case "Low":
        return "green";
      default:
        return "gray";
    }
  };

  return (
    <div className="container">
      <h1>AI Bug Severity Predictor</h1>

      <textarea
        placeholder="Enter error message..."
        value={errorMessage}
        onChange={(e) => setErrorMessage(e.target.value)}
      />

      <button onClick={handlePredict} disabled={loading}>
        {loading ? "Predicting..." : "Predict Severity"}
      </button>

      {error && <p className="error">{error}</p>}

      {result && (
        <div className="result">
          <h3>Prediction Result</h3>
          <p>
            Severity:{" "}
            <span
              style={{
                color: getSeverityColor(result.severity),
                fontWeight: "bold"
              }}
            >
              {result.severity}
            </span>
          </p>
          <p>
            Confidence: {(result.confidence * 100).toFixed(2)}%
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
