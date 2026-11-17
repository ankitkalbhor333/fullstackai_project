const express = require("express");
const path = require("path");
const { createProxyMiddleware } = require("http-proxy-middleware");

const app = express();
const PORT = process.env.PORT || 3000;
const BACKEND_URL = process.env.BACKEND_URL || "http://127.0.0.1:8000";

// 1. Proxy API requests (/detect and /api/*) to the Python FastAPI backend
const apiProxy = createProxyMiddleware({
  target: BACKEND_URL,
  changeOrigin: true,
  onError: (err, req, res) => {
    console.error("Proxy error to backend:", err.message);
    res.status(502).json({
      error: "Cannot connect to backend server at " + BACKEND_URL,
      hint: "Make sure the Python FastAPI backend (anti_campaign_detector/main.py) is running on port 8000.",
    });
  },
});

app.use("/detect", apiProxy);
app.use("/api", apiProxy);

// 2. Serve static files from the React build directory
const buildPath = path.join(__dirname, "build");
app.use(express.static(buildPath));

// 3. Fallback for React SPA client-side routing
app.get("*", (req, res) => {
  const indexPath = path.join(buildPath, "index.html");
  res.sendFile(indexPath, (err) => {
    if (err) {
      res.status(500).send(
        "Build not found or error loading index.html. Run 'npm run build' first."
      );
    }
  });
});

app.listen(PORT, () => {
  console.log(`====================================================`);
  console.log(`🚀 Dashboard server running at: http://localhost:${PORT}`);
  console.log(`📡 API requests (/detect) proxy to: ${BACKEND_URL}`);
  console.log(`💡 Ensure Python backend is running: python main.py`);
  console.log(`====================================================`);
});
