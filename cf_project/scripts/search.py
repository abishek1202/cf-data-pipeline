import chromadb
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to DB
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_collection(name="cf_data")


def search(query):
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    return results["documents"]


if __name__ == "__main__":

    query = input("Ask something: ")

    results = search(query)

    print("\n✅ Results:\n")

    for r in results:
        print(r)

