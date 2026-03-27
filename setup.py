import os
import sys

sys.path.append(os.path.abspath(os.path.abspath(__file__)))

def setup():
    db_path = "data/inventory.db"
    chroma_path = "data/chroma_db"

    os.makedirs("data", exist_ok=True)

    if not os.path.exists(db_path):
        print("Setting up inventory database...")
        from data.seed import seed_products
        seed_products()

    if not os.path.exists(chroma_path):
        print("Setting up ChromaDB for RAG...")
        from data.ingest import ingest_products
        ingest_products()

if __name__ == "__main__":
    setup()
