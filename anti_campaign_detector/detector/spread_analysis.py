import networkx as nx
from detector.similarity import detect_text_similarity
from detector.timeburst import detect_time_bursts
from collections import Counter
import pandas as pd

def find_seeds(posts, top_n=5):
    if not posts:
        return []
    sorted_posts = sorted(posts, key=lambda x: x.get("createdAt", ""))
    return [p.get("user_id", "") for p in sorted_posts[:top_n] if p.get("user_id")]

def find_amplifiers(posts, interval="30min"):
    if not posts:
        return []
    df = pd.DataFrame(posts)
    if "createdAt" not in df.columns:
        return []
    df["timestamp"] = pd.to_datetime(df["createdAt"], errors="coerce")
    df = df.dropna(subset=["timestamp"])
    if df.empty:
        return []

    burst_counts = df.groupby(pd.Grouper(key="timestamp", freq=interval)).size()
    burst_windows = burst_counts[burst_counts > burst_counts.mean()].index

    amplifiers = []
    for post in posts:
        ts = pd.to_datetime(post.get("createdAt", ""), errors="coerce")
        if pd.isna(ts):
            continue
        if any(abs((ts - bw).total_seconds()) < 1800 for bw in burst_windows):
            amplifiers.append(post.get("user_id", ""))
    return list(set(a for a in amplifiers if a))

def find_influencers(posts):
    if not posts:
        return {}
    G = nx.Graph()
    for post in posts:
        acc = post.get("user_id", "")
        for tag in post.get("hashtags", []):
            G.add_edge(acc, tag)
    if len(G) == 0:
        return {}
    centrality = nx.degree_centrality(G)
    return dict(sorted(centrality.items(), key=lambda x: x[1], reverse=True))

def cluster_similar_accounts(posts, threshold=0.7):
    if not posts:
        return {}
    pairs = detect_text_similarity(posts, threshold)
    clusters = {}
    for pair in pairs:
        clusters.setdefault(pair["post_1"], []).append(pair["post_2"])
    return clusters

def score_spreaders(posts):
    if not posts:
        return {}

    seeds = find_seeds(posts)
    amplifiers = find_amplifiers(posts)
    centrality = find_influencers(posts)
    similarity_clusters = cluster_similar_accounts(posts)

    all_accounts = set(p.get("user_id", "") for p in posts if p.get("user_id"))
    scores = {}

    for acc in all_accounts:
        is_seed = 1 if acc in seeds else 0
        is_amplifier = 1 if acc in amplifiers else 0
        graph_score = centrality.get(acc, 0)
        similarity_cluster_size = len(similarity_clusters.get(acc, []))

        score = (
            2 * is_seed +
            2 * is_amplifier +
            3 * graph_score +
            1 * similarity_cluster_size
        )
        scores[acc] = round(score, 2)

    return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))

