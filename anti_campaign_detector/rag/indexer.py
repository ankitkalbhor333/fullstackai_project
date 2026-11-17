"""
RAG Indexer — Indexes local JSON posts data into Pinecone.

Usage:
    python -m rag.indexer

Loads posts from anti_campaign_detector/data/retrieved_posts.json,
embeds them using Google Gemini text-embedding-004, and upserts
the vectors into the Pinecone 'ragapi' index.
"""

import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from pinecone import Pinecone

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "ragapi").strip()

BATCH_SIZE = 50
BATCH_DELAY_SECONDS = 1.5  # small delay between batches to avoid rate limits

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "retrieved_posts.json"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _load_posts() -> list[dict]:
    """Load posts from the local JSON file and normalise into a flat list."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Data file not found: {DATA_PATH}")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    posts: list[dict] = []

    if isinstance(data, dict):
        for user_id, user_info in data.items():
            username = user_info.get("username", user_id)
            for post in user_info.get("posts", []):
                posts.append({
                    "account": username,
                    "text": post.get("content", ""),
                    "hashtags": post.get("hashtags", []),
                    "timestamp": post.get("createdAt", ""),
                })
    elif isinstance(data, list):
        for post in data:
            posts.append({
                "account": post.get("account", post.get("username", "")),
                "text": post.get("text", post.get("content", "")),
                "hashtags": post.get("hashtags", []),
                "timestamp": post.get("timestamp", post.get("createdAt", "")),
            })

    return posts


def _post_to_text(post: dict) -> str:
    """Convert a post dict into a single text document for embedding."""
    hashtags_str = ", ".join(post.get("hashtags", []))
    return (
        f"[{post.get('account', '')}] {post.get('text', '')} "
        f"| Hashtags: {hashtags_str} "
        f"| Time: {post.get('timestamp', '')}"
    )


# ---------------------------------------------------------------------------
# Main indexing logic
# ---------------------------------------------------------------------------

def index_posts() -> None:
    """Embed all posts and upsert them into Pinecone."""
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is not set in the environment.")
    if not PINECONE_API_KEY:
        raise RuntimeError("PINECONE_API_KEY is not set in the environment.")

    # Load posts
    posts = _load_posts()
    if not posts:
        print("[INDEXER] No posts found — nothing to index.")
        return

    print(f"[INDEXER] Loaded {len(posts)} posts from {DATA_PATH.name}")

    # Initialise clients
    gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index = pc.Index(PINECONE_INDEX_NAME)

    # Process in batches
    for batch_start in range(0, len(posts), BATCH_SIZE):
        batch = posts[batch_start : batch_start + BATCH_SIZE]
        texts = [_post_to_text(p) for p in batch]

        # Embed the batch
        result = gemini_client.models.embed_content(
            model="text-embedding-004",
            contents=texts,
        )

        # Build upsert vectors
        vectors = []
        for i, (post, embedding) in enumerate(zip(batch, result.embeddings)):
            vec_id = f"post-{batch_start + i}"
            vectors.append({
                "id": vec_id,
                "values": embedding.values,
                "metadata": {
                    "account": post.get("account", ""),
                    "text": post.get("text", ""),
                    "hashtags": json.dumps(post.get("hashtags", [])),
                    "timestamp": post.get("timestamp", ""),
                },
            })

        # Upsert into Pinecone
        index.upsert(vectors=vectors)
        batch_end = min(batch_start + BATCH_SIZE, len(posts))
        print(f"[INDEXER] Upserted batch {batch_start}–{batch_end} ({len(vectors)} vectors)")

        # Rate-limit delay between batches
        if batch_end < len(posts):
            time.sleep(BATCH_DELAY_SECONDS)

    print(f"[INDEXER] Done — indexed {len(posts)} posts into '{PINECONE_INDEX_NAME}'.")


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    index_posts()
