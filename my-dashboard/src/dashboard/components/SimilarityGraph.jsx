// src/dashboard/components/SimilarityGraph.jsx
import React from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from "recharts";

const SimilarityGraph = ({ data }) => {
  const chartData = (data && data.length > 0)
    ? data.slice(0, 10).map((p) => ({
        pair: `${p.post_1}-${p.post_2}`,
        similarity: p.similarity,
      }))
    : [];

  return (
    <div className="chart-card">
      <h3>🔗 Post Similarity Graph</h3>
      {chartData.length === 0 ? (
        <p style={{ textAlign: "center", color: "#888", padding: "20px" }}>
          No highly similar post pairs detected (threshold &gt;= 0.7)
        </p>
      ) : (
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="pair" />
            <YAxis domain={[0, 1]} />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="similarity" stroke="#8884d8" strokeWidth={3} />
          </LineChart>
        </ResponsiveContainer>
      )}
    </div>
  );
};

export default SimilarityGraph;
