# ============================================
# FREE LLM QUERY SYSTEM (IMPROVED)
# ============================================

import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline


# ============================================
# LOAD VECTOR DATABASE
# ============================================
def load_vector_db():
    try:
        embedding = HuggingFaceEmbeddings()

        db = Chroma(
            persist_directory="vector_db",
            embedding_function=embedding
        )

        print("✅ Vector DB loaded successfully")
        return db

    except Exception as e:
        print(f"❌ Error loading DB: {e}")
        return None


# ============================================
# RETRIEVE DATA FROM DB
# ============================================
def retrieve_context(db, query):
    try:
        results = db.similarity_search(query, k=5)

        context = "\n\n".join([r.page_content for r in results])

        return context

    except Exception as e:
        print(f"❌ Retrieval error: {e}")
        return ""


# ============================================
# LOAD LOCAL LLM (FIXED ✅)
# ============================================
def load_llm():
    print("⚙️ Loading free LLM model...")

    generator = pipeline(
        "text-generation",   # ✅ FIXED
        model="google/flan-t5-base",
        max_length=200
    )

    print("✅ LLM loaded successfully")
    return generator


# ============================================
# GENERATE ANSWER (IMPROVED ✅)
# ============================================
def generate_answer(llm, context, query):
    try:
        if not context:
            return "❌ No data found in database."

        query_lower = query.lower()

        keyword_map = {
            "delay": "delay",
            "deliver": "deliver",
            "transit": "transit",
            "price": "price"
        }

        target = None
        for key in keyword_map:
            if key in query_lower:
                target = keyword_map[key]
                break

        sentences = context.split("\n\n")

        # ✅ Keyword filtering
        if target:
            filtered = [
                s.strip() for s in sentences
                if target in s.lower()
            ]

            filtered = list(set(filtered))

            if filtered:
                return "\n\n".join(filtered)
            else:
                return f"No {target} related information found."

        # ✅ LLM fallback
        prompt = f"""
You are a supply chain assistant.

Answer only using the given data.

DATA:
{context}

QUESTION:
{query}

ANSWER:
"""

        response = llm(prompt)
        return response[0]["generated_text"]

    except Exception as e:
        print(f"❌ Error: {e}")
        return "Error generating answer"


# ============================================
# MAIN PROGRAM
# ============================================
if __name__ == "__main__":

    print("\n🚀 FREE LLM QUERY SYSTEM STARTED\n")

    db = load_vector_db()

    if db is None:
        print("❌ DB load failed. Exiting...")
        exit()

    llm = load_llm()

    while True:
        query = input("\n💬 Ask your question (type 'exit' to quit): ")

        if query.lower() == "exit":
            print("👋 Exiting...")
            break

        # Step 1: Retrieve
        context = retrieve_context(db, query)

        # Step 2: Answer
        answer = generate_answer(llm, context, query)

        print("\n✅ Answer:\n")
        print(answer)
        print("\n" + "="*50)