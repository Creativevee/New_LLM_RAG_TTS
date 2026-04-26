from typing import Dict, List

from config import TOP_K
from ingest import embedder, get_collection


def retrieve(query: str, k: int = TOP_K) -> List[Dict]:
    if not query.strip():
        return []
    coll = get_collection()
    if coll.count() == 0:
        return []
    q_embed = embedder.encode([query]).tolist()
    result = coll.query(query_embeddings=q_embed, n_results=min(k, coll.count()))
    docs = result.get("documents", [[]])[0]
    metas = result.get("metadatas", [[]])[0]
    distances = result.get("distances", [[]])[0]
    return [
        {"text": d, "doc": m.get("doc", ""), "score": round(1 - dist, 4)}
        for d, m, dist in zip(docs, metas, distances)
    ]
