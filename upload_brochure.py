from time import sleep
from pathlib import Path
import re
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec

BROCHURE_PATH = Path(__file__).with_name("laptop.txt")
INDEX_NAME = "laptop-store"
NAMESPACE = "brochure"
EMBEDDING_DIMENSION = 384

# Connect Pinecone
pc = Pinecone(api_key="pcsk_48jDm4_584oZ99PotkGzMF7Ck6hjkYAPadDYFe2h65btYtTNdutqYgAHAJAnJnDNEV6oG6")

if not pc.has_index(INDEX_NAME):
    pc.create_index(
        name=INDEX_NAME,
        dimension=EMBEDDING_DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

while not pc.describe_index(INDEX_NAME).status["ready"]:
    sleep(1)

index = pc.Index(INDEX_NAME)

# Embedding model
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# Read brochure
brochure = BROCHURE_PATH.read_text(encoding="utf-8").strip()

if not brochure:
    raise ValueError("laptop.txt is empty. Add brochure text before uploading.")


chunks = [chunk.strip() for chunk in re.split(r"\n\n+", brochure) if chunk.strip()]

# Create embedding

vectors = []

for i, chunk in enumerate(chunks):
    if chunk.strip():
        embedding = model.encode(chunk).tolist()

        vectors.append({
            "id": f"chunk-{i}",
            "values": embedding,
            "metadata": {
                "text": chunk
            }
        })

# Store in Pinecone
try:
    index.delete(delete_all=True, namespace=NAMESPACE)
except Exception as e:
    if "Namespace not found" not in str(e):
        raise

index.upsert(vectors=vectors, namespace=NAMESPACE)

stats = index.describe_index_stats()
print("Index stats:", stats)

print("Brochure uploaded")
