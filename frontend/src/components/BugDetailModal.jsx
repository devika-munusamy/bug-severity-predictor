import React from "react";

export default function BugDetailModal({ bug, onClose }) {
  if (!bug) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>&times;</button>
        
        <div className="modal-header">
          <span className={`badge badge-${bug.predicted_severity.toLowerCase()}`}>
            {bug.predicted_severity} Severity
          </span>
          <span className="modal-time">{new Date(bug.timestamp.replace(" ", "T") + "Z").toLocaleString()}</span>
        </div>

        <h3 className="modal-title">Bug Details</h3>
        <p className="modal-msg">{bug.error_message}</p>

        <div className="modal-grid">
          <div className="modal-stat">
            <span className="stat-lbl">Category</span>
            <span className="stat-val">{bug.error_category}</span>
          </div>
          <div className="modal-stat">
            <span className="stat-lbl">Impact Score</span>
            <span className="stat-val">{bug.impact_score}</span>
          </div>
          <div className="modal-stat">
            <span className="stat-lbl">Users Affected</span>
            <span className="stat-val">{bug.user_count}</span>
          </div>
        </div>

        {bug.root_cause && (
          <div className="rca-card" style={{ marginTop: '1.5rem', animation: 'none' }}>
            <div className="rca-section">
              <span className="rca-section-label">Root Cause Analysis</span>
              <p className="rca-section-text">{bug.root_cause}</p>
            </div>
            {bug.suggested_fix && (
              <div className="rca-section" style={{ marginTop: '1rem' }}>
                <span className="rca-section-label">Suggested Fixes</span>
                <pre className="rca-fix-steps">{bug.suggested_fix}</pre>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
