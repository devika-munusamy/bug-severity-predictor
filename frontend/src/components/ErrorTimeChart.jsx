import React from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="chart-tooltip">
        <p className="tooltip-time">{label}</p>
        <p className="tooltip-count">
          <span className="tooltip-dot" />
          {payload[0].value} error{payload[0].value !== 1 ? "s" : ""}
        </p>
      </div>
    );
  }
  return null;
};

export default function ErrorTimeChart({ timeSeries = [] }) {
  // Show last 15 buckets to keep the chart readable
  const data = timeSeries.slice(-15).map((d) => {
    // d.bucket is "YYYY-MM-DD HH:MM", assumed UTC from backend
    const utcStr = d.bucket.replace(" ", "T") + "Z";
    const date = new Date(utcStr);

    // Format to "HH:MM" in local time
    const time = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    return {
      time: time,
      count: d.count,
    };
  });

  return (
    <div className="chart-card">
      <h3 className="chart-title">⏱ Error Rate – Last 15 Minutes</h3>
      <ResponsiveContainer width="100%" height={220}>
        <AreaChart data={data} margin={{ top: 10, right: 16, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id="errorGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%"  stopColor="#6366f1" stopOpacity={0.4} />
              <stop offset="95%" stopColor="#6366f1" stopOpacity={0.02} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis
            dataKey="time"
            tick={{ fill: "#94a3b8", fontSize: 11 }}
            interval="preserveStartEnd"
          />
          <YAxis
            allowDecimals={false}
            tick={{ fill: "#94a3b8", fontSize: 11 }}
            width={28}
          />
          <Tooltip content={<CustomTooltip />} />
          <Area
            type="monotone"
            dataKey="count"
            stroke="#6366f1"
            strokeWidth={2}
            fill="url(#errorGradient)"
            dot={false}
            activeDot={{ r: 5, fill: "#6366f1" }}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
