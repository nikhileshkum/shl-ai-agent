import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

# -----------------------------------
# LOAD MODEL
# -----------------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# -----------------------------------
# LOAD FAISS INDEX
# -----------------------------------

index = faiss.read_index(
    "vector_store/shl.index"
)

# -----------------------------------
# LOAD CATALOG
# -----------------------------------

with open(
    "catalog.json",
    "r",
    encoding="utf-8"
) as f:

    catalog = json.load(f)

# -----------------------------------
# TECH KEYWORDS
# -----------------------------------

TECH_KEYWORDS = [
    "java",
    "python",
    "aws",
    "docker",
    "spring",
    "sql",
    "backend",
    "frontend",
    "api",
    "cloud",
    "kubernetes",
    "devops"
]

# -----------------------------------
# SEARCH FUNCTION
# -----------------------------------

def search_assessments(query, top_k=15):

    query_lower = query.lower()

    # -----------------------------------
    # CREATE QUERY EMBEDDING
    # -----------------------------------

    query_embedding = model.encode(
        [query],
        normalize_embeddings=True
    )

    query_embedding = np.array(
        query_embedding
    ).astype("float32")

    faiss.normalize_L2(query_embedding)

    # -----------------------------------
    # SEARCH VECTOR DB
    # -----------------------------------

    scores, indices = index.search(
        query_embedding,
        top_k
    )

    recommendations = []

    seen = set()

    # -----------------------------------
    # DETECT TECHNICAL QUERY
    # -----------------------------------

    query_is_technical = any(
        word in query_lower
        for word in TECH_KEYWORDS
    )

    # -----------------------------------
    # PROCESS RESULTS
    # -----------------------------------

    for idx in indices[0]:

        if idx >= len(catalog):
            continue

        item = catalog[idx]

        name = item.get("name", "")
        description = item.get("description", "")
        keys = " ".join(item.get("keys", []))

        searchable_text = f"""
        {name}
        {description}
        {keys}
        """.lower()

        # -----------------------------------
        # REMOVE NOISY RESULTS
        # -----------------------------------

        if query_is_technical:

            blocked_words = [
                "remoteworkq",
                "participant report",
                "manager report",
                "behavior",
                "personality"
            ]

            if any(
                blocked in searchable_text
                for blocked in blocked_words
            ):
                continue

        # -----------------------------------
        # QUERY WORD MATCH
        # -----------------------------------

        query_words = [
            word
            for word in query_lower.split()
            if len(word) > 2
        ]

        matched_count = sum(
            1
            for word in query_words
            if word in searchable_text
        )

        matched = matched_count >= 1

        if not matched:
            continue

        # -----------------------------------
        # TECH STACK MATCH BOOST
        # -----------------------------------

        tech_score = sum(
            1
            for tech in TECH_KEYWORDS
            if tech in searchable_text
            and tech in query_lower
        )

        if query_is_technical and tech_score == 0:
            continue

        # -----------------------------------
        # REMOVE DUPLICATES
        # -----------------------------------

        if name in seen:
            continue

        seen.add(name)

        # -----------------------------------
        # ADD RESULT
        # -----------------------------------

        recommendations.append({
            "name": name,
            "url": item.get("link", ""),
            "test_type": (
                item["keys"][0]
                if item.get("keys")
                else "Unknown"
            )
        })

        # -----------------------------------
        # LIMIT RESULTS
        # -----------------------------------

        if len(recommendations) >= 5:
            break

    return recommendations