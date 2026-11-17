from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from retriever.rag_pipeline import retrieve
from detector.frequency import detect_frequent_hashtags, detect_top_accounts
from detector.similarity import detect_text_similarity
from detector.spread_analysis import score_spreaders
from detector.timeburst import detect_time_bursts
from detector.graph_detect import detect_graph_clusters

app = FastAPI()

# Allow React frontend to connect (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def calculate_threat_score(posts, similar_posts, time_bursts, graph_clusters, top_spreaders):
    """
    Calculate a 0-100 campaign threat score from combined algorithm outputs.

    Breakdown:
      - Volume        (0-15): Number of matching posts found
      - Similarity    (0-30): Ratio of similar pairs to max possible pairs
      - Burst         (0-20): How concentrated posts are in few time windows
      - Coordination  (0-15): How tightly accounts cluster via shared hashtags
      - Spreaders     (0-20): Strength of top spreader scores
    """
    if not posts:
        return {"score": 0, "level": "None", "breakdown": {}}

    n = len(posts)

    # --- Volume score (0-15) ---
    volume = min(n / 40, 1.0) * 15

    # --- Similarity score (0-30) ---
    max_pairs = n * (n - 1) / 2 if n >= 2 else 1
    sim_count = len(similar_posts) if similar_posts else 0
    similarity = min(sim_count / max_pairs, 1.0) * 30

    # --- Burst score (0-20) ---
    if time_bursts and isinstance(time_bursts, dict):
        burst_values = list(time_bursts.values())
        total_in_bursts = sum(burst_values)
        max_in_single = max(burst_values) if burst_values else 0
        # Concentration: what fraction of posts are in the biggest window
        concentration = max_in_single / n if n > 0 else 0
        burst = concentration * 20
    else:
        burst = 0

    # --- Coordination score (0-15) ---
    if graph_clusters and isinstance(graph_clusters, list):
        largest_cluster = max(len(c) for c in graph_clusters) if graph_clusters else 0
        unique_accounts = len(set(p.get("username", "") for p in posts))
        # If most accounts are in one cluster, high coordination
        coordination = min(largest_cluster / max(unique_accounts + 5, 1), 1.0) * 15
    else:
        coordination = 0

    # --- Spreader score (0-20) ---
    if top_spreaders and isinstance(top_spreaders, dict):
        spreader_values = list(top_spreaders.values())
        max_spread = max(spreader_values) if spreader_values else 0
        spreaders = min(max_spread / 50, 1.0) * 20
    else:
        spreaders = 0

    total = round(volume + similarity + burst + coordination + spreaders, 1)
    total = min(total, 100)

    # Determine threat level
    if total >= 75:
        level = "Critical"
    elif total >= 50:
        level = "High"
    elif total >= 25:
        level = "Moderate"
    elif total > 0:
        level = "Low"
    else:
        level = "None"

    return {
        "score": total,
        "level": level,
        "breakdown": {
            "volume": round(volume, 1),
            "similarity": round(similarity, 1),
            "burst": round(burst, 1),
            "coordination": round(coordination, 1),
            "spreaders": round(spreaders, 1),
        }
    }


@app.get("/")
def root():
    return {"status": "ok", "service": "Disinformation Detection Platform API"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/detect")
def detect_campaign(query: str = "khalistan"):
    posts = retrieve(query)
    similar_posts = detect_text_similarity(posts)
    time_bursts = detect_time_bursts(posts)
    graph_clusters = detect_graph_clusters(posts)
    top_spreaders = score_spreaders(posts)

    threat = calculate_threat_score(posts, similar_posts, time_bursts, graph_clusters, top_spreaders)

    return {
        "query": query,
        "totalPosts": len(posts),
        "threatScore": threat,
        "retrievedPosts": posts,
        "topHashtags": detect_frequent_hashtags(posts),
        "topAccounts": detect_top_accounts(posts),
        "similarPosts": similar_posts,
        "timeBursts": time_bursts,
        "graphClusters": graph_clusters,
        "topSpreaders": top_spreaders,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
