import { useEffect, useState } from "react";
import "./dashboard.css";

import PostsTable from "./components/PostsTable";
import HashtagChart from "./components/TopHashtags";
import AccountsChart from "./components/AccountsChart";
import SimilarityGraph from "./components/SimilarityGraph";
import ClusterGraph from "./components/ClusterGraph";
import FrequencyChart from "./components/FrequencyChart";
import SpreadersChart from "./components/SpreadersChart";
import AISummary from "./components/AISummary";

const Dashboard = () => {
  const [query, setQuery] = useState("khalistan"); // default search
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // function to fetch data
  const fetchData = (searchQuery) => {
    setLoading(true);
    setError(null);
    const backendBase = process.env.REACT_APP_API_URL || "http://localhost:8001";
    fetch(`${backendBase}/detect?query=${encodeURIComponent(searchQuery)}`)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`Server returned HTTP ${res.status}`);
        }
        return res.json();
      })
      .then((resData) => {
        setData(resData);
        setError(null);
      })
      .catch((err) => {
        console.error("API Error:", err);
        setError(`Failed to connect to backend: ${err.message}. Make sure Python FastAPI is running on port 8001.`);
      })
      .finally(() => setLoading(false));
  };

  // fetch default query on first load
  useEffect(() => {
    fetchData("khalistan");
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    if (query.trim() !== "") {
      fetchData(query);
    }
  };

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">📊 Campaign Detection Dashboard</h1>

      {/* 🔎 Search Bar */}
      <form onSubmit={handleSearch} className="search-bar">
        <input
          type="text"
          placeholder="Enter query (e.g. khalistan)"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit">Search</button>
      </form>

      {loading && <h2>Loading analysis...</h2>}

      {error && (
        <div style={{ background: "#fee2e2", color: "#b91c1c", padding: "14px", borderRadius: "8px", margin: "16px 0", textAlign: "center", border: "1px solid #f87171" }}>
          {error}
        </div>
      )}

      {!loading && data && (
        <>
          <div className="dashboard-section">
            <PostsTable posts={data.retrievedPosts} />
          </div>

          <div className="dashboard-grid">
            <HashtagChart data={data.topHashtags} />
            <AccountsChart data={data.topAccounts} />
          </div>

          <div className="dashboard-grid">
            <FrequencyChart posts={data.retrievedPosts} />
            <SpreadersChart data={data.topSpreaders} />
          </div>

          <div className="dashboard-grid">
            <SimilarityGraph data={data.similarPosts} />
            <ClusterGraph data={data.graphClusters} />
          </div>
        </>
      )}
    </div>
  );
};

export default Dashboard;
