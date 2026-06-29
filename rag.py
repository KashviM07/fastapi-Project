
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

pc = Pinecone(
    api_key="pcsk_48jDm4_584oZ99PotkGzMF7Ck6hjkYAPadDYFe2h65btYtTNdutqYgAHAJAnJnDNEV6oG6"
)

index = pc.Index("laptop-store")
NAMESPACE = "brochure"

def retrieve_context(question):
    query_vector = model.encode(question).tolist()

    results = index.query(
        vector=query_vector,
        top_k=5,
        include_metadata=True,
        namespace=NAMESPACE
    )

    matches = results.get("matches", [])

    matches = [m for m in matches if m["score"] > 0.3]

    print("Pinecone matches:", [(m["score"], m["metadata"]["text"][:50]) for m in matches])

    if not matches:
        return "No relevant context found."

    return "\n".join(
        match["metadata"]["text"]
        for match in matches
    )
