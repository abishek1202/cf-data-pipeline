# ============================================
# LLM QUERY SYSTEM (FREE - NO OPENAI)
# ============================================

import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# ✅ FREE LOCAL LLM
from transformers import pipeline


# ============================================
# LOAD VECTOR DATABASE
# ============================================
def load_vector_db():
    try:
        embedding = HuggingFaceEmbeddings() # used to convert text into vector embeddings

        db = Chroma(
            persist_directory="vector_db",
            embedding_function=embedding # save vectors and metadata in a local directory
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
        results = db.similarity_search(query, k=10)

        context = "\n\n".join([r.page_content for r in results])

        return context

    except Exception as e:
        print(f"❌ Retrieval error: {e}")
        return ""


# ============================================
# LOAD LOCAL LLM (FREE)
# ============================================
def load_llm():
    print("⚙️ Loading free LLM model... (first time may take 1-2 minutes)")

    generator = pipeline(
        "text-generation",
        model="google/flan-t5-base",   # ✅ FREE ai model
        max_length=200
    )

    print("✅ LLM loaded successfully")
    return generator # ai model for generating answers


# ============================================
# CREATE PROMPT
# ============================================
def create_prompt(context, query):

    prompt = f"""
    You are a supply chain assistant.

    Based only on the following data, answer the question clearly.

    DATA:
    {context}

    QUESTION:
    {query}

    ANSWER:
    """

    return prompt


# ============================================
# GENERATE ANSWER
# ============================================
def generate_answer(llm, context, query):
    try:
        # ✅ Step 1: Convert query to lowercase
        query_lower = query.lower()

        # ✅ Step 2: Decide what to filter
        if "delay" in query_lower:
            target = "Delayed"
        elif "deliver" in query_lower:
            target = "Delivered"
        elif "transit" in query_lower:
            target = "In Transit"
        elif "price" in query_lower:
            target = "In price"
        else:
            # ✅ fallback → show retrieved context
            return context

        # ✅ Step 3: Split into sentences
        sentences = context.split("\n\n") # assuming each record is separated by double newlines, adjust if needed

        # ✅ Step 4: Filter based on target
        filtered = [s.strip() for s in sentences if target in s]

        # ✅ Step 5: Remove duplicates
        filtered = list(set(filtered))

        # ✅ Step 6: Return result
        if filtered:
            return "\n\n".join(filtered)

        return f"No {target.lower()} shipments found."

    except Exception as e:
        print(f"❌ Error: {e}")
        return "Error generating answer"


# ============================================
# MAIN PROGRAM
# ============================================
if __name__ == "__main__":

    print("\n🚀 FREE LLM QUERY SYSTEM STARTED\n")

    db = load_vector_db()
    llm = load_llm()

    while True:
        query = input("\n💬 Ask your question (type 'exit' to quit): ")

        if query.lower() == "exit":
            print("👋 Exiting...")
            break

        # Step 1: Retrieve data
        context = retrieve_context(db, query)
        
        # Step 2: Generate answer
        answer = generate_answer(llm, context, query)

        print("\n✅ Answer:\n")
        print(answer)
        print("\n" + "="*50)