import React, { useEffect, useState, useCallback, useMemo } from "react";
import { io } from "socket.io-client";
import HistoryTable from "../components/HistoryTable";
import SeverityChart from "../components/SeverityChart";
import ErrorTimeChart from "../components/ErrorTimeChart";
import BugDetailModal from "../components/BugDetailModal";

export default function Dashboard() {
  const [history, setHistory] = useState([]);
  const [anomaly, setAnomaly] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [selectedBug, setSelectedBug] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const [severityFilter, setSeverityFilter] = useState("All");
  const [sourceFilter, setSourceFilter] = useState("All");

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

  // WebSocket for Live Monitoring
  useEffect(() => {
    const socket = io("http://127.0.0.1:5000");

    socket.on("new_bug", (newBug) => {
      console.log("Live Bug Received:", newBug);
      // Prepend the new bug to the history list
      setHistory((prev) => [newBug, ...prev]);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

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

  // Filter Logic
  const filteredHistory = useMemo(() => {
    return history.filter(bug => {
      // Severity Match
      const matchSev = severityFilter === "All" || bug.predicted_severity === severityFilter;
      // Source Match (Extracting [app_source] using quick logic, or just substring if we prefer)
      const msgLower = bug.error_message.toLowerCase();
      const matchSource = sourceFilter === "All" || msgLower.includes(`[${sourceFilter.toLowerCase()}]`);
      // Keyword Match
      const matchSearch = searchQuery === "" || msgLower.includes(searchQuery.toLowerCase()) || 
                          (bug.root_cause && bug.root_cause.toLowerCase().includes(searchQuery.toLowerCase()));
      return matchSev && matchSource && matchSearch;
    });
  }, [history, severityFilter, sourceFilter, searchQuery]);

  // Unique sources for dropdown
  const sources = useMemo(() => {
    const s = new Set(["All"]);
    history.forEach(h => {
      const match = h.error_message.match(/^\[(.*?)\]/);
      if (match) s.add(match[1]);
    });
    return Array.from(s);
  }, [history]);

  // CSV Export
  const exportToCSV = () => {
    if (!filteredHistory.length) return;
    const headers = ["Timestamp", "Error Message", "Category", "Users", "Severity", "Impact Score"];
    const rows = filteredHistory.map(r => 
      [r.timestamp, `"${r.error_message.replace(/"/g, '""')}"`, r.error_category, r.user_count, r.predicted_severity, r.impact_score].join(",")
    );
    const csvContent = "data:text/csv;charset=utf-8," + [headers.join(","), ...rows].join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `bug_history_${new Date().toISOString()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

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

      {/* ── Filter Panel ── */}
      <div className="filter-panel">
        <div className="filter-group">
          <input 
            type="text" 
            className="filter-input" 
            placeholder="Search errors or causes..." 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <select className="filter-select" value={severityFilter} onChange={(e) => setSeverityFilter(e.target.value)}>
            <option value="All">All Severities</option>
            <option value="High">High</option>
            <option value="Medium">Medium</option>
            <option value="Low">Low</option>
          </select>
          <select className="filter-select" value={sourceFilter} onChange={(e) => setSourceFilter(e.target.value)}>
            {sources.map(src => <option key={src} value={src}>{src === "All" ? "All Sources" : src}</option>)}
          </select>
        </div>
        <button className="btn-export" onClick={exportToCSV}>📥 Export CSV</button>
      </div>

      {/* ── History Table ── */}
      {loading ? (
        <p className="loading-msg">Loading…</p>
      ) : (
        <HistoryTable history={filteredHistory} onRowClick={setSelectedBug} />
      )}

      {/* ── Bug Detail Modal ── */}
      <BugDetailModal bug={selectedBug} onClose={() => setSelectedBug(null)} />
    </div>
  );
}
