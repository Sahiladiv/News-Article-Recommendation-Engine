import chromadb
from sentence_transformers import SentenceTransformer

# Loading model once
model = SentenceTransformer("all-MiniLM-L6-v2")

# Loading Chroma client and collection
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection("news_articles_vectors")

def get_recommendations(query_text: str, top_n: int = 5):
    query_embedding = model.encode([query_text])[0].tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_n
    )

    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    recommendations = []
    for meta, score in zip(metadatas, distances):
        print(meta)
        similarity = round(1 - score, 3)  # Chroma returns Euclidean distance
        recommendations.append({
            "headline": meta["headline"],
            "category": meta["category"],
            "authors": meta["authors"],
            "description": meta["description"],
            "link": meta["link"],
            # "date": meta["date"]
        })

    return recommendations
