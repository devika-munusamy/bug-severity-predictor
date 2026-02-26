import React, { useEffect, useState, useCallback } from "react";
import HistoryTable from "../components/HistoryTable";
import SeverityChart from "../components/SeverityChart";
import ErrorTimeChart from "../components/ErrorTimeChart";

export default function Dashboard() {
  const [history, setHistory] = useState([]);
  const [anomaly, setAnomaly] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetchAll = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const [histRes, anomalyRes] = await Promise.all([
        fetch("http://127.0.0.1:5000/history"),
        fetch("http://127.0.0.1:5000/anomaly-status"),
      ]);
      const histData    = await histRes.json();
      const anomalyData = await anomalyRes.json();
      setHistory(histData);
      setAnomaly(anomalyData);
    } catch {
      setError("Could not load data. Is the backend running?");
    }
    setLoading(false);
  }, []);

  useEffect(() => { fetchAll(); }, [fetchAll]);

  // Auto-refresh anomaly status every 30 s
  useEffect(() => {
    const id = setInterval(async () => {
      try {
        const res  = await fetch("http://127.0.0.1:5000/anomaly-status");
        const data = await res.json();
        setAnomaly(data);
      } catch { /* silent */ }
    }, 30_000);
    return () => clearInterval(id);
  }, []);

  return (
    <div className="dashboard-page">

      {/* ── Header ── */}
      <div className="dashboard-header">
        <h2 className="page-title">📊 AI Bug Intelligence Dashboard</h2>
        <button className="btn-refresh" onClick={fetchAll}>↻ Refresh</button>
      </div>

      {error && <p className="error-msg">{error}</p>}

      {/* ── Anomaly Alert Banner ── */}
      {anomaly && (
        <div className={`anomaly-banner ${anomaly.is_anomaly ? "anomaly-alert" : "anomaly-ok"}`}>
          <span className="anomaly-banner-icon">
            {anomaly.is_anomaly ? "🚨" : "✅"}
          </span>
          <div className="anomaly-banner-text">
            <strong>{anomaly.is_anomaly ? "Anomaly Detected!" : "System Normal"}</strong>
            <span>
              {anomaly.is_anomaly
                ? ` Current error rate (${anomaly.current_count}/min) exceeds the expected range of ${anomaly.expected_range[0]}–${anomaly.expected_range[1]}.`
                : ` Error rate is within the expected range (${anomaly.expected_range[0]}–${anomaly.expected_range[1]} per min). Currently: ${anomaly.current_count}/min.`}
            </span>
            <span className="anomaly-method-badge">{anomaly.method}</span>
          </div>
        </div>
      )}

      {/* ── Charts Row ── */}
      <div className="dashboard-grid">
        <SeverityChart history={history} />
        <div className="stats-row">
          {["High", "Medium", "Low"].map((level) => {
            const count  = history.filter((r) => r.predicted_severity === level).length;
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

      {/* ── Error Time-Series Chart ── */}
      {anomaly && (
        <ErrorTimeChart timeSeries={anomaly.time_series} />
      )}

      {/* ── History Table ── */}
      {loading ? (
        <p className="loading-msg">Loading…</p>
      ) : (
        <HistoryTable history={history} />
      )}
    </div>
  );
}
