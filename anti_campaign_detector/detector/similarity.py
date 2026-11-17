from sentence_transformers import SentenceTransformer, util

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def detect_text_similarity(posts, threshold=0.7):
    if not posts or len(posts) < 2:
        return []

    model = get_model()
    texts = [p.get("content", "") for p in posts]
    accounts = [p.get("user_id", f"user_{i}") for i, p in enumerate(posts)]

    embeddings = model.encode(texts, convert_to_tensor=True)
    cosine_scores = util.pytorch_cos_sim(embeddings, embeddings)

    similar_pairs = []
    for i in range(len(posts)):
        for j in range(i + 1, len(posts)):
            score = cosine_scores[i][j].item()
            if score >= threshold:
                similar_pairs.append({
                    "post_1": accounts[i],
                    "post_2": accounts[j],
                    "similarity": round(score, 2)
                })

    return similar_pairs

