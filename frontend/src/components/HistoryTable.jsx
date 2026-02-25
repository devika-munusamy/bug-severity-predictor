import React from "react";

const SEVERITY_CLASS = { High: "badge-high", Medium: "badge-medium", Low: "badge-low" };

export default function HistoryTable({ history }) {
  if (!history.length) {
    return <p className="empty-msg">No predictions yet. Go to Predict to get started!</p>;
  }

  return (
    <div className="table-wrapper">
      <table className="history-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Timestamp (UTC)</th>
            <th>Error Message</th>
            <th>Users</th>
            <th>Severity</th>
            <th>Confidence</th>
            <th>Impact Score</th>
          </tr>
        </thead>
        <tbody>
          {history.map((row, idx) => (
            <tr key={row.id}>
              <td>{idx + 1}</td>
              <td className="col-time">{row.timestamp}</td>
              <td className="col-msg">{row.error_message}</td>
              <td>{row.user_count}</td>
              <td>
                <span className={`badge ${SEVERITY_CLASS[row.predicted_severity]}`}>
                  {row.predicted_severity}
                </span>
              </td>
              <td>{(row.confidence * 100).toFixed(1)}%</td>
              <td>{row.impact_score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
