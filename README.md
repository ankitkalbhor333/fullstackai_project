# SATI CyberShield - Disinformation Detection Platform

A real-time disinformation campaign detection platform that retrieves social media posts, analyzes coordinated behavior patterns, and visualizes results through an interactive dashboard.

## Project Structure

```
ragproject/
├── anti_campaign_detector/       # Python FastAPI Backend (port 8000)
│   ├── main.py                   # FastAPI server & API endpoints
│   ├── requirements.txt          # Python dependencies
│   ├── data/
│   │   └── retrieved_posts.json  # Offline fallback dataset
│   ├── retriever/
│   │   └── rag_pipeline.py       # Data retrieval (API + local fallback)
│   ├── detector/
│   │   ├── frequency.py          # Hashtag & account frequency analysis
│   │   ├── similarity.py         # Text similarity (SentenceTransformers)
│   │   ├── timeburst.py          # Temporal burst detection
│   │   ├── graph_detect.py       # Account-hashtag graph clustering
│   │   └── spread_analysis.py    # Seed/amplifier/influencer scoring
│   ├── templates/
│   │   └── index.html            # Simple HTML detection page
│   └── utils/
│       └── helpers.py            # Utility functions
│
├── my-dashboard/                 # React Frontend Dashboard (port 3000)
│   ├── server.js                 # Production Express server + API proxy
│   ├── package.json
│   └── src/
│       └── dashboard/
│           ├── Dashboard.jsx     # Main dashboard with search
│           └── components/
│               ├── PostsTable.jsx
│               ├── TopHashtags.jsx
│               ├── AccountsChart.jsx
│               ├── FrequencyChart.jsx
│               ├── SpreadersChart.jsx
│               ├── SimilarityGraph.jsx
│               └── ClusterGraph.jsx
│
├── start_platform.bat            # One-click launcher (Windows)
├── start_platform.ps1            # One-click launcher (PowerShell)
└── README.md                     # This file
```

## Quick Start

### Option 1: One-Click Launch
Double-click `start_platform.bat` — opens both backend and frontend automatically.

### Option 2: Manual Launch

**Terminal 1 — Backend:**
```bash
cd anti_campaign_detector
.\venv\Scripts\python.exe main.py
# Running at http://localhost:8000
```

**Terminal 2 — Frontend:**
```bash
cd my-dashboard
npm run serve
# Running at http://localhost:3000
```

Then open **http://localhost:3000** in your browser.

## Features

- **Hashtag & Account Frequency Analysis** — Top trending hashtags and most active accounts
- **Text Similarity Detection** — Semantic cosine similarity using SentenceTransformers (all-MiniLM-L6-v2)
- **Time Burst Detection** — Identifies coordinated posting spikes
- **Graph Cluster Analysis** — NetworkX-based account-hashtag relationship mapping
- **Spread Analysis** — Composite threat scoring (seeds, amplifiers, influencers, similarity clusters)
- **RAG Pipeline** — Live API retrieval with offline fallback
- **Interactive Dashboard** — Real-time search and visualization with Recharts

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Service status |
| `/health` | GET | Health check |
| `/detect?query=khalistan` | GET | Run full campaign detection analysis |

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI, Uvicorn |
| NLP | SentenceTransformers, PyTorch |
| Graph Analysis | NetworkX |
| Data Processing | Pandas, scikit-learn |
| Frontend | React 19, Recharts, React Router |
| Server | Node.js, Express, http-proxy-middleware |
