import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="data/chroma_db")
collection = client.get_collection("products")
model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_products(query: str, top_k: int = 3) -> str:
    embedding = model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )

    docs = results["documents"][0]
    metadatas = results["metadatas"][0]

    if not docs:
        return "No relevant products found"
    
    output = []
    for i, (doc, meta) in enumerate(zip(docs, metadatas)):
        output.append(f"{i+1}. {doc}")
    
    return "\n".join(output)

if __name__ == "__main__":
    test_query = "heavy duty power supply compatible with 220V"
    print(f"Query: {test_query}\n")
    print(retrieve_products(test_query))