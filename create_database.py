import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
from tqdm import tqdm 

df = pd.read_json("dataset/news_article_dataset.json", lines=True)
df.dropna(subset=["headline", "short_description", "authors"], inplace=True)
df["text"] = df["headline"] + " " + df["short_description"]

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection("news_articles_vectors")

# Encoding the text and adding it to Chroma database
print("Adding to ChromaDB...")
BATCH_SIZE = 32
for i in tqdm(range(0, len(df), BATCH_SIZE), desc="Storing in batches"):
    batch_df = df.iloc[i:i + BATCH_SIZE]
    batch_texts = batch_df["text"].tolist()
    batch_embeddings = model.encode(batch_texts).tolist()

    collection.add(
        documents=batch_texts,
        metadatas=[{
            "headline": row["headline"],
            "category": row["category"],
            "authors": row["authors"],
            "description": row["short_description"],
            "link": row["link"]
        } for _, row in batch_df.iterrows()],
        ids=[f"doc_{idx}" for idx in batch_df.index],
        embeddings=batch_embeddings
    )

print("✅ All embeddings stored successfully!")

