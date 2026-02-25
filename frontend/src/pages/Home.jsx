import React, { useState } from "react";

const SEVERITY_COLOR = { High: "#ef4444", Medium: "#f97316", Low: "#22c55e" };

export default function Home() {
  const [errorMessage, setErrorMessage] = useState("");
  const [userCount, setUserCount] = useState(1);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handlePredict = async () => {
    if (!errorMessage.trim()) {
      setError("Please enter an error message.");
      return;
    }
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const res = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ error_message: errorMessage, user_count: Number(userCount) }),
      });
      const data = await res.json();
      if (data.error) throw new Error(data.error);
      setResult(data);
    } catch (err) {
      setError(err.message || "Server not reachable. Is the backend running?");
    }
    setLoading(false);
  };

  return (
    <div className="page-center">
      <div className="predict-card">
        <h2 className="card-title">🔍 Predict Bug Severity</h2>

        <label className="field-label">Error Message</label>
        <textarea
          className="input-textarea"
          placeholder="e.g. Database connection refused on checkout..."
          value={errorMessage}
          onChange={(e) => setErrorMessage(e.target.value)}
          rows={4}
        />

        <label className="field-label">Affected Users</label>
        <input
          className="input-number"
          type="number"
          min={1}
          value={userCount}
          onChange={(e) => setUserCount(e.target.value)}
        />

        <button className="btn-predict" onClick={handlePredict} disabled={loading}>
          {loading ? "Analyzing…" : "Predict Severity"}
        </button>

        {error && <p className="error-msg">{error}</p>}

        {result && (
          <div className="result-card">
            <h3 className="result-heading">Prediction Result</h3>
            <div className="result-grid">
              <div className="result-item">
                <span className="result-label">Severity</span>
                <span
                  className="result-value severity-pill"
                  style={{ background: SEVERITY_COLOR[result.severity] }}
                >
                  {result.severity}
                </span>
              </div>
              <div className="result-item">
                <span className="result-label">Confidence</span>
                <span className="result-value">{(result.confidence * 100).toFixed(2)}%</span>
              </div>
              <div className="result-item">
                <span className="result-label">Impact Score</span>
                <span className="result-value">{result.impact_score}</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
