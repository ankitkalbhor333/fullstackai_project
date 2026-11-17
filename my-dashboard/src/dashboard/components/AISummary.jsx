import React from "react";

const AISummary = ({ summary }) => {
  if (!summary) return null;

  return (
    <div
      style={{
        background: "linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)",
        borderLeft: "4px solid #6c63ff",
        borderRadius: "12px",
        padding: "24px",
        marginBottom: "20px",
        color: "#e0e0e0",
        boxShadow: "0 4px 15px rgba(108, 99, 255, 0.15)",
      }}
    >
      <h2 style={{ color: "#6c63ff", marginTop: 0, marginBottom: "16px", fontSize: "1.3rem" }}>
        🤖 AI Threat Analysis
      </h2>
      <div
        style={{
          whiteSpace: "pre-wrap",
          lineHeight: "1.7",
          fontSize: "0.95rem",
          fontFamily: "'Segoe UI', system-ui, sans-serif",
        }}
      >
        {summary}
      </div>
      <div
        style={{
          textAlign: "right",
          marginTop: "16px",
          fontSize: "0.75rem",
          color: "#888",
          fontStyle: "italic",
        }}
      >
        Powered by Gemini AI
      </div>
    </div>
  );
};

export default AISummary;
