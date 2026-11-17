import { useEffect, useRef } from "react";

const ThreatBadge = ({ threatScore }) => {
  const canvasRef = useRef(null);

  if (!threatScore || threatScore.score === undefined) return null;

  const { score, level, breakdown } = threatScore;

  // Color based on threat level
  const getColor = () => {
    if (score >= 75) return { main: "#dc2626", bg: "#fef2f2", border: "#fca5a5", glow: "rgba(220,38,38,0.3)" };
    if (score >= 50) return { main: "#ea580c", bg: "#fff7ed", border: "#fdba74", glow: "rgba(234,88,12,0.3)" };
    if (score >= 25) return { main: "#d97706", bg: "#fffbeb", border: "#fcd34d", glow: "rgba(217,119,6,0.3)" };
    return { main: "#16a34a", bg: "#f0fdf4", border: "#86efac", glow: "rgba(22,163,74,0.3)" };
  };

  const colors = getColor();

  const getLevelEmoji = () => {
    if (score >= 75) return "\uD83D\uDED1"; // 🛑
    if (score >= 50) return "\u26A0\uFE0F"; // ⚠️
    if (score >= 25) return "\uD83D\uDFE1"; // 🟡
    return "\uD83D\uDFE2"; // 🟢
  };

  // Draw gauge arc on canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const size = 140;
    canvas.width = size;
    canvas.height = size * 0.65;

    const cx = size / 2;
    const cy = size * 0.58;
    const radius = size * 0.4;
    const startAngle = Math.PI;
    const endAngle = 2 * Math.PI;

    // Background arc
    ctx.beginPath();
    ctx.arc(cx, cy, radius, startAngle, endAngle);
    ctx.strokeStyle = "#e5e7eb";
    ctx.lineWidth = 12;
    ctx.lineCap = "round";
    ctx.stroke();

    // Score arc
    const scoreAngle = startAngle + (score / 100) * Math.PI;
    ctx.beginPath();
    ctx.arc(cx, cy, radius, startAngle, scoreAngle);
    ctx.strokeStyle = colors.main;
    ctx.lineWidth = 12;
    ctx.lineCap = "round";
    ctx.stroke();

    // Score text
    ctx.font = "bold 28px Inter, sans-serif";
    ctx.fillStyle = colors.main;
    ctx.textAlign = "center";
    ctx.textBaseline = "bottom";
    ctx.fillText(Math.round(score), cx, cy + 4);

    // "/100" text
    ctx.font = "12px Inter, sans-serif";
    ctx.fillStyle = "#9ca3af";
    ctx.fillText("/100", cx, cy + 18);
  }, [score, colors.main]);

  const breakdownItems = breakdown ? [
    { label: "Volume", value: breakdown.volume, max: 15, desc: "Post count" },
    { label: "Similarity", value: breakdown.similarity, max: 30, desc: "Content overlap" },
    { label: "Burst", value: breakdown.burst, max: 20, desc: "Time concentration" },
    { label: "Coordination", value: breakdown.coordination, max: 15, desc: "Network clustering" },
    { label: "Spreaders", value: breakdown.spreaders, max: 20, desc: "Amplifier strength" },
  ] : [];

  return (
    <div style={{
      background: colors.bg,
      border: `2px solid ${colors.border}`,
      borderRadius: "16px",
      padding: "24px",
      marginBottom: "28px",
      boxShadow: `0 4px 24px ${colors.glow}`,
      display: "flex",
      alignItems: "center",
      gap: "32px",
      flexWrap: "wrap",
    }}>
      {/* Gauge */}
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", minWidth: "150px" }}>
        <canvas ref={canvasRef} style={{ marginBottom: "4px" }} />
        <div style={{
          fontSize: "1.1rem",
          fontWeight: 700,
          color: colors.main,
          display: "flex",
          alignItems: "center",
          gap: "6px",
        }}>
          {getLevelEmoji()} {level} Threat
        </div>
      </div>

      {/* Breakdown bars */}
      <div style={{ flex: 1, minWidth: "280px" }}>
        <div style={{ fontSize: "0.85rem", fontWeight: 600, color: "#6b7280", marginBottom: "10px", textTransform: "uppercase", letterSpacing: "0.5px" }}>
          Score Breakdown
        </div>
        {breakdownItems.map((item) => (
          <div key={item.label} style={{ marginBottom: "8px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.82rem", marginBottom: "3px" }}>
              <span style={{ fontWeight: 500, color: "#374151" }}>{item.label} <span style={{ color: "#9ca3af", fontWeight: 400 }}>({item.desc})</span></span>
              <span style={{ fontWeight: 600, color: colors.main }}>{item.value}/{item.max}</span>
            </div>
            <div style={{ height: "6px", background: "#e5e7eb", borderRadius: "3px", overflow: "hidden" }}>
              <div style={{
                height: "100%",
                width: `${(item.value / item.max) * 100}%`,
                background: colors.main,
                borderRadius: "3px",
                transition: "width 0.6s ease",
              }} />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ThreatBadge;
