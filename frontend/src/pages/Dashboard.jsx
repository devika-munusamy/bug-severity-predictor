import React, { useEffect, useState } from "react";
import HistoryTable from "../components/HistoryTable";
import SeverityChart from "../components/SeverityChart";

export default function Dashboard() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:5000/history");
      const data = await res.json();
      setHistory(data);
    } catch {
      setError("Could not load history. Is the backend running?");
    }
    setLoading(false);
  };

  useEffect(() => { fetchHistory(); }, []);

  return (
    <div className="dashboard-page">
      <div className="dashboard-header">
        <h2 className="page-title">📊 Bug Intelligence Dashboard</h2>
        <button className="btn-refresh" onClick={fetchHistory}>↻ Refresh</button>
      </div>

      {error && <p className="error-msg">{error}</p>}

      <div className="dashboard-grid">
        <SeverityChart history={history} />

        <div className="stats-row">
          {["High", "Medium", "Low"].map((level) => {
            const count = history.filter((r) => r.predicted_severity === level).length;
            const colors = { High: "#ef4444", Medium: "#f97316", Low: "#22c55e" };
            return (
              <div key={level} className="stat-card" style={{ borderColor: colors[level] }}>
                <span className="stat-number" style={{ color: colors[level] }}>{count}</span>
                <span className="stat-label">{level} Severity</span>
              </div>
            );
          })}
        </div>
      </div>

      {loading ? (
        <p className="loading-msg">Loading history…</p>
      ) : (
        <HistoryTable history={history} />
      )}
    </div>
  );
}
