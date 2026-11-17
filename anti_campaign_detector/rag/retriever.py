"""
RAG Retriever — Semantic search via Pinecone + AI summary via Gemini.

Provides:
    rag_retrieve(query, top_k)      – vector-similarity search over indexed posts
    generate_ai_summary(...)        – LLM-powered threat analysis summary
"""

import json
import os
from collections import Counter
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


# ---------------------------------------------------------------------------
# Semantic retrieval
# ---------------------------------------------------------------------------

def rag_retrieve(query: str, top_k: int = 15) -> list[dict]:
    """
    Embed *query* with Gemini text-embedding-004 and return the
    top_k most similar posts from Pinecone.

    Returns a list of dicts with keys:
        account, text, hashtags, timestamp, similarity_score
    """
    try:
        if not GEMINI_API_KEY or not PINECONE_API_KEY:
            print("[RAG] WARNING: API keys not configured — skipping RAG retrieval.")
            return []

        # Embed the query
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        embed_result = gemini_client.models.embed_content(
            model="text-embedding-004",
            contents=[query],
        )
        query_vector = embed_result.embeddings[0].values

        # Query Pinecone
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index = pc.Index(PINECONE_INDEX_NAME)
        response = index.query(vector=query_vector, top_k=top_k, include_metadata=True)

        results: list[dict] = []
        for match in response.get("matches", []):
            meta = match.get("metadata", {})
            # hashtags are stored as JSON string in metadata
            hashtags = meta.get("hashtags", "[]")
            if isinstance(hashtags, str):
                try:
                    hashtags = json.loads(hashtags)
                except json.JSONDecodeError:
                    hashtags = []

            results.append({
                "account": meta.get("account", ""),
                "text": meta.get("text", ""),
                "hashtags": hashtags,
                "timestamp": meta.get("timestamp", ""),
                "similarity_score": round(match.get("score", 0.0), 4),
            })

        print(f"[RAG] Retrieved {len(results)} posts for query '{query}'")
        return results

    except Exception as exc:
        print(f"[RAG] WARNING: RAG retrieval failed — {exc}")
        return []


# ---------------------------------------------------------------------------
# AI-powered threat summary
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = (
    "You are a cybersecurity analyst specializing in disinformation campaign "
    "detection on social media. Analyze the following data and provide a concise "
    "threat assessment. Be specific about patterns, coordination indicators, and "
    "risk level. Format your response in clear sections."
)


def generate_ai_summary(
    query: str,
    posts: list,
    threat_score: dict,
    similar_posts: list,
    time_bursts: dict,
    top_spreaders: dict,
) -> str:
    """
    Use Gemini 2.0 Flash to generate a human-readable threat analysis summary
    from the detection pipeline outputs.
    """
    try:
        if not GEMINI_API_KEY:
            return "AI summary unavailable — GEMINI_API_KEY not configured."

        # --- Build top hashtags ------------------------------------------------
        hashtag_counter: Counter = Counter()
        for post in posts:
            for tag in post.get("hashtags", []):
                hashtag_counter[tag] += 1
        top_hashtags = hashtag_counter.most_common(10)

        # --- Compose user prompt -----------------------------------------------
        breakdown = threat_score.get("breakdown", {})
        user_prompt = (
            f"## Query: {query}\n\n"
            f"**Total posts analysed:** {len(posts)}\n\n"
            f"### Threat Score\n"
            f"- Overall: {threat_score.get('score', 'N/A')} / 100 "
            f"({threat_score.get('level', 'N/A')})\n"
            f"- Volume: {breakdown.get('volume', 'N/A')}\n"
            f"- Similarity: {breakdown.get('similarity', 'N/A')}\n"
            f"- Burst: {breakdown.get('burst', 'N/A')}\n"
            f"- Coordination: {breakdown.get('coordination', 'N/A')}\n"
            f"- Spreaders: {breakdown.get('spreaders', 'N/A')}\n\n"
            f"### Top Hashtags\n"
            f"{chr(10).join(f'- {tag}: {cnt}' for tag, cnt in top_hashtags)}\n\n"
            f"### Top Spreaders\n"
            f"{chr(10).join(f'- {acct}: {score}' for acct, score in (top_spreaders or {}).items())}\n\n"
            f"### Similar Post Pairs\n"
            f"Number of similar-content post pairs detected: {len(similar_posts) if similar_posts else 0}\n\n"
            f"### Time Burst Windows\n"
            f"{chr(10).join(f'- {window}: {count} posts' for window, count in (time_bursts or {}).items())}\n\n"
            f"Provide your threat assessment below."
        )

        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        response = gemini_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"{SYSTEM_PROMPT}\n\n{user_prompt}",
        )
        return response.text

    except Exception as exc:
        print(f"[RAG] WARNING: AI summary generation failed — {exc}")
        return "AI summary could not be generated at this time. Please review the numerical analysis above."
