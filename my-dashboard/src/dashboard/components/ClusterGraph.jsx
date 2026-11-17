// src/dashboard/components/ClusterGraph.jsx
import React from "react";
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts";

const ClusterGraph = ({ data }) => {
  const clusters = Array.isArray(data) ? data : [];

  const points = [];
  clusters.slice(0, 6).forEach((cluster, cIdx) => {
    cluster.forEach((member, mIdx) => {
      points.push({
        x: (cIdx + 1) * 20 + ((mIdx * 7) % 15),
        y: ((mIdx * 11) % 80) + 10,
        cluster: `Cluster ${cIdx + 1}`,
        member: member,
        clusterSize: cluster.length,
      });
    });
  });

  return (
    <div className="chart-card">
      <h3>🧩 Graph Clusters ({clusters.length} detected)</h3>
      {points.length === 0 ? (
        <p style={{ textAlign: "center", color: "#888", padding: "20px" }}>
          No graph clusters detected
        </p>
      ) : (
        <ResponsiveContainer width="100%" height={300}>
          <ScatterChart>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis type="number" dataKey="x" name="Cluster Dimension" />
            <YAxis type="number" dataKey="y" name="Degree Factor" />
            <Tooltip
              cursor={{ strokeDasharray: "3 3" }}
              content={({ payload }) => {
                if (!payload || payload.length === 0) return null;
                const d = payload[0].payload;
                return (
                  <div style={{ background: "#fff", border: "1px solid #ccc", padding: "8px", borderRadius: "4px" }}>
                    <strong>{d.cluster}</strong> ({d.clusterSize} nodes)<br />
                    <span>Node: {d.member}</span>
                  </div>
                );
              }}
            />
            <Scatter name="Cluster Nodes" data={points} fill="#82ca9d" />
          </ScatterChart>
        </ResponsiveContainer>
      )}
    </div>
  );
};

export default ClusterGraph;
