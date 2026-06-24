# ============================================
# SIMPLE STREAMLIT UI (BASIC VERSION)
# ============================================

import streamlit as st

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


# ============================================
# LOAD VECTOR DB
# ============================================
@st.cache_resource
def load_db():
    embedding = HuggingFaceEmbeddings()

    db = Chroma(
        persist_directory="vector_db",
        embedding_function=embedding
    )

    return db


# ============================================
# RETRIEVE CONTEXT
# ============================================
def retrieve_context(db, query):
    results = db.similarity_search(query, k=5)
    context = "\n\n".join([r.page_content for r in results])
    return context


# ============================================
# SIMPLE ANSWER LOGIC
# ============================================
def generate_answer(context, query):

    query_lower = query.lower()

    if "delay" in query_lower:
        target = "Delayed"
    elif "deliver" in query_lower:
        target = "Delivered"
    else:
        return context

    sentences = context.split("\n\n")
    filtered = [s for s in sentences if target in s]

    filtered = list(set(filtered))

    if filtered:
        return "\n\n".join(filtered)

    return "No matching results found."


# ============================================
# UI
# ============================================

st.title("📦 C&F AI Query App")

st.write("Ask questions about shipments or inventory")

# Load DB
db = load_db()

# Input
query = st.text_input("Enter your question:")

# Button
if st.button("Get Answer"):

    if query:

        with st.spinner("Processing...."):

            context = retrieve_context(db, query)
            answer = generate_answer(context, query)

        st.subheader("✅ Answer:")
        st.write(answer)

        # Debug section
        with st.expander("See retrieved data"):
            st.write(context)

    else:
        st.warning("Please enter a query")
