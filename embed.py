import json
import faiss
import numpy as np
import os

from sentence_transformers import SentenceTransformer

# -----------------------------------
# CREATE VECTOR STORE FOLDER
# -----------------------------------

os.makedirs("vector_store", exist_ok=True)

# -----------------------------------
# LOAD EMBEDDING MODEL
# -----------------------------------

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# -----------------------------------
# LOAD DATASET
# -----------------------------------

with open(
    "catalog.json",
    "r",
    encoding="utf-8"
) as f:

    catalog = json.load(f)

# -----------------------------------
# CREATE SEARCHABLE TEXT
# -----------------------------------

texts = []

for item in catalog:

    text = f"""
    Assessment Name:
    {item.get('name', '')}

    Description:
    {item.get('description', '')}

    Skills:
    {' '.join(item.get('keys', []))}

    Job Levels:
    {' '.join(item.get('job_levels', []))}
    """

    texts.append(text)

# -----------------------------------
# GENERATE EMBEDDINGS
# -----------------------------------

embeddings = model.encode(
    texts,
    normalize_embeddings=True
)

# -----------------------------------
# CONVERT TO NUMPY
# -----------------------------------

embeddings = np.array(
    embeddings
).astype("float32")

# -----------------------------------
# NORMALIZE FOR BETTER SEARCH
# -----------------------------------

faiss.normalize_L2(embeddings)

# -----------------------------------
# CREATE FAISS INDEX
# -----------------------------------

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(embeddings)

# -----------------------------------
# SAVE INDEX
# -----------------------------------

faiss.write_index(
    index,
    "vector_store/shl.index"
)

print("FAISS index created successfully!")