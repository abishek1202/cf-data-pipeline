import chromadb
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# ✅ Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Load FREE LLM
generator = pipeline(
    task="text-generation",
    model="distilgpt2"
)



# ✅ Connect to vector DB
client_db = chromadb.PersistentClient(path="chroma_db")
collection = client_db.get_collection(name="cf_data")


# ✅ Retrieve data
def retrieve_data(query):
    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    return results["documents"][0]


# ✅ FREE LLM
def ask_llm(query, context):

    prompt = f"""You are a supply chain expert.

Based only on the data below, answer the question.

Data:
{context}

Question: {query}

Give ONLY the final answer. Do not repeat instructions.
"""

    result = generator(prompt, max_new_tokens=50)

    output = result[0]["generated_text"]

    # Clean output
    output = output.replace(prompt, "").strip()

    if "Answer the question" in output:
        output = output.split("\n")[-1].strip()

    return output


# ✅ MAIN LOOP
if __name__ == "__main__":

    print("\n🤖 FREE AI Assistant Ready (type 'exit' to quit)\n")

    while True:
        query = input("Ask your data: ")

        if query.lower() == "exit":
            break

        results = retrieve_data(query)

        context = "\n".join(results)

        answer = ask_llm(query, context)

        print("\n✅ Answer:\n", answer)