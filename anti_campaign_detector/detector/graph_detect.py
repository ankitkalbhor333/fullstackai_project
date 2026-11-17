import networkx as nx

def detect_graph_clusters(posts):
    if not posts:
        return []
    G = nx.Graph()
    for post in posts:
        acc = post.get("user_id") or post.get("username", "")
        if not acc:
            continue
        for tag in post.get("hashtags", []):
            if tag:
                G.add_edge(acc, tag)
    if len(G) == 0:
        return []
    return [sorted(list(c)) for c in nx.connected_components(G)]

