import json
from pathlib import Path


def load_data():
    """Load post data from the local JSON dataset."""
    local_path = Path(__file__).resolve().parent.parent / "data" / "retrieved_posts.json"
    if local_path.exists():
        with open(local_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"[DATA] Loaded {len(data)} posts from local file: {local_path.name}")
            return data
    print("[WARN] Local data file not found.")
    return {}


def retrieve(query: str):
    """Filter posts matching the query by username, content, or hashtags."""
    data = load_data()
    results = []
    q = (query or "").strip().lower()

    if isinstance(data, dict):
        for user_id, user_info in data.items():
            username = user_info.get("username", user_id)
            for post in user_info.get("posts", []):
                content = post.get("content", "")
                hashtags = post.get("hashtags", [])
                created_at = post.get("createdAt", "")
                if (
                    not q
                    or q in username.lower()
                    or q in content.lower()
                    or any(q in h.lower() for h in hashtags)
                ):
                    results.append({
                        "user_id": user_id,
                        "username": username,
                        "content": content,
                        "hashtags": hashtags,
                        "createdAt": created_at,
                    })

    elif isinstance(data, list):
        for idx, post in enumerate(data):
            username = post.get("account", post.get("username", f"user{idx:03d}"))
            user_id = post.get("user_id", username)
            content = post.get("text", post.get("content", ""))
            hashtags = post.get("hashtags", [])
            created_at = post.get("timestamp", post.get("createdAt", ""))
            if (
                not q
                or q in username.lower()
                or q in content.lower()
                or any(q in h.lower() for h in hashtags)
            ):
                results.append({
                    "user_id": user_id,
                    "username": username,
                    "content": content,
                    "hashtags": hashtags,
                    "createdAt": created_at,
                })

    return results


if __name__ == "__main__":
    query = "#Khalistan"
    results = retrieve(query)
    print(f"Retrieved {len(results)} posts for query '{query}':")
    print(json.dumps(results, indent=2))
