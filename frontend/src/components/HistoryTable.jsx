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
            <th>Timestamp (Local)</th>
            <th>Error Message</th>
            <th>Category</th>
            <th>Users</th>
            <th>Severity</th>
            <th>Confidence</th>
            <th>Impact Score</th>
          </tr>
        </thead>
        <tbody>
          {history.map((row, idx) => {
            // Ensure format like YYYY-MM-DDTHH:MM:SSZ so JS Date parses it correctly in UTC
            const localTime = new Date(row.timestamp.replace(" ", "T") + "Z").toLocaleString();
            return (
            <tr key={row.id}>
              <td>{idx + 1}</td>
              <td className="col-time">{localTime}</td>
              <td className="col-msg">{row.error_message}</td>
              <td>
                <span className="category-tag">
                  {row.error_category || "—"}
                </span>
              </td>
              <td>{row.user_count}</td>
              <td>
                <span className={`badge ${SEVERITY_CLASS[row.predicted_severity]}`}>
                  {row.predicted_severity}
                </span>
              </td>
              <td>{(row.confidence * 100).toFixed(1)}%</td>
              <td>{row.impact_score}</td>
            </tr>
          );
          })}
        </tbody>
      </table>
    </div>
  );
}
