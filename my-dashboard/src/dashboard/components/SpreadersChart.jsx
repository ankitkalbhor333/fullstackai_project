import React from "react";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const SpreadersChart = ({ data }) => {
  if (!data || Object.keys(data).length === 0) {
    return (
      <div className="card">
        <h2>🚀 Top Spreaders</h2>
        <p style={{ textAlign: "center", color: "#888", padding: "20px" }}>No spreaders detected</p>
      </div>
    );
  }

  const formatted = Object.entries(data).slice(0, 10).map(([user, score]) => ({ user, score }));

  return (
    <div className="card">
      <h2>🚀 Top Spreaders</h2>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={formatted}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="user" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="score" fill="#FF5733" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SpreadersChart;
