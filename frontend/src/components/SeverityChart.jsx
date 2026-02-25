import React from "react";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Cell, ResponsiveContainer, Legend,
} from "recharts";

const COLORS = { High: "#ef4444", Medium: "#f97316", Low: "#22c55e" };

export default function SeverityChart({ history }) {
  const counts = history.reduce(
    (acc, r) => {
      acc[r.predicted_severity] = (acc[r.predicted_severity] || 0) + 1;
      return acc;
    },
    { High: 0, Medium: 0, Low: 0 }
  );

  const chartData = [
    { name: "High", count: counts.High },
    { name: "Medium", count: counts.Medium },
    { name: "Low", count: counts.Low },
  ];

  return (
    <div className="chart-card">
      <h3 className="chart-title">Severity Distribution</h3>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={chartData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="name" tick={{ fill: "#94a3b8" }} />
          <YAxis allowDecimals={false} tick={{ fill: "#94a3b8" }} />
          <Tooltip
            contentStyle={{ background: "#1e293b", border: "1px solid #334155", borderRadius: 8 }}
            labelStyle={{ color: "#f1f5f9" }}
          />
          <Legend />
          <Bar dataKey="count" radius={[6, 6, 0, 0]}>
            {chartData.map((entry) => (
              <Cell key={entry.name} fill={COLORS[entry.name]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
