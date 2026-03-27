import sqlite3
import os
import chromadb
from sentence_transformers import SentenceTransformer

def ingest_products():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, description FROM products")
    products = cursor.fetchall()
    conn.close()

    client = chromadb.PersistentClient(path="data/chroma_db")

    try:
        client.delete_collection("products")
    except:
        pass

    collection = client.create_collection("products")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    ids, documents, embeddings, metadatas = [], [], [], []

    for product in products:
        pid, name, category, description = product
        text = f"{name}. Category: {category}. {description}"
        embedding = model.encode(text).tolist()
        ids.append(str(pid))
        documents.append(text)
        embeddings.append(embedding)
        metadatas.append({"name": name, "category": category})

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )
    print(f"Ingested {len(products)} products into ChromaDB.")

if __name__ == "__main__":
    ingest_products()