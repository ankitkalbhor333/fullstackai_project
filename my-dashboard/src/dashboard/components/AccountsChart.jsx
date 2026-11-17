import React from "react";
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from "recharts";

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#aa66cc"];

const AccountsChart = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <div className="card">
        <h2>👤 Top Accounts</h2>
        <p style={{ textAlign: "center", color: "#888", padding: "20px" }}>No accounts available</p>
      </div>
    );
  }

  const formatted = data.map((item) => ({
    acc: item.username || item.user_id || "Unknown",
    posts: item.post_count || 1,
  }));

  return (
    <div className="card">
      <h2>👤 Top Accounts</h2>
      <ResponsiveContainer width="100%" height={250}>
        <PieChart>
          <Pie
            data={formatted}
            dataKey="posts"
            nameKey="acc"
            outerRadius={90}
            label={(entry) => `${entry.acc} (${entry.posts})`}
          >
            {formatted.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default AccountsChart;

