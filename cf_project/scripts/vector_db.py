import os
import sys

import chromadb
from sentence_transformers import SentenceTransformer
from prepare_data import load_data, convert_to_text

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load data
inventory, shipment, invoice = load_data()
documents = convert_to_text(inventory, shipment, invoice)

# Create vector DB
client = chromadb.PersistentClient(path="chroma_db")
collection = client.create_collection(name="cf_data")

# Store embeddings
for i, doc in enumerate(documents):
    embedding = model.encode(doc).tolist()

    collection.add(
        ids=[str(i)],
        documents=[doc],
        embeddings=[embedding]
    )

print("✅ Data stored in Vector DB")