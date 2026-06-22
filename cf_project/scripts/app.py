# ============================================
# SIMPLE STREAMLIT UI (BASIC VERSION)
# ============================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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

        with st.spinner("Processing..."):

            context = retrieve_context(db, query)
            answer = generate_answer(context, query)

        st.subheader("✅ Answer:")
        st.write(answer)

        # Debug section
        with st.expander("See retrieved data"):
            st.write(context)

    else:
        st.warning("Please enter a query")
        
# ============================================
# SIDEBAR
# ============================================
st.sidebar.title("📊 Navigation")

option = st.sidebar.radio(
    "Select Option",
    ["Ask AI", "Dashboard", "Sample Queries", "About Project"]
)


# ============================================
# 1. ASK AI
# ============================================
if option == "Ask AI":

    st.title("📦 C&F AI Assistant")
    st.markdown("Ask questions about **Shipments & Inventory**")

    query = st.text_input("💬 Enter your question:")

    if st.button("🚀 Get Answer"):

        if query:

            with st.spinner("🔍 Fetching data..."):

                context = retrieve_context(db, query)
                answer = generate_answer(context, query)

            st.success("✅ Answer Generated")

            st.subheader("📌 Answer")
            st.write(answer)

            with st.expander("🔍 Retrieved Data"):
                st.code(context)

        else:
            st.warning("⚠️ Please enter a query")


# ============================================
# 2. INTERACTIVE DASHBOARD
# ============================================
elif option == "Dashboard":

    st.title("📊 Interactive C&F Dashboard")

    try:
        shipment_df = pd.read_csv("data/processed/shipment_processed.csv")
        inventory_df = pd.read_csv("data/processed/inventory_processed.csv")

    except:
        st.error("❌ Processed data not found. Run pipeline first.")
        st.stop()

    # ✅ FILTERS
    st.sidebar.subheader("🔍 Filters")

    status_filter = st.sidebar.multiselect(
        "Shipment Status",
        options=shipment_df["shipment_status"].unique(),
        default=shipment_df["shipment_status"].unique()
    )

    warehouse_filter = st.sidebar.multiselect(
        "Warehouse",
        options=inventory_df["warehouse_location"].unique(),
        default=inventory_df["warehouse_location"].unique()
    )

    shipment_filtered = shipment_df[
        shipment_df["shipment_status"].isin(status_filter)
    ]

    inventory_filtered = inventory_df[
        inventory_df["warehouse_location"].isin(warehouse_filter)
    ]

    # ✅ KPI METRICS
    st.subheader("📌 Key Metrics")

    total_shipments = len(shipment_filtered)
    delayed = len(shipment_filtered[shipment_filtered["shipment_status"] == "Delayed"])
    delivered = len(shipment_filtered[shipment_filtered["shipment_status"] == "Delivered"])

    total_products = len(inventory_filtered)
    total_value = inventory_filtered["total_value"].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("🚚 Shipments", total_shipments)
    col2.metric("⚠️ Delayed", delayed)
    col3.metric("✅ Delivered", delivered)

    col4, col5 = st.columns(2)
    col4.metric("📦 Products", total_products)
    col5.metric("💰 Inventory Value", int(total_value))

    st.markdown("---")

    # ✅ PIE CHART
    st.subheader("🚚 Shipment Status Distribution")

    status_counts = shipment_filtered["shipment_status"].value_counts()

    fig, ax = plt.subplots()
    ax.pie(status_counts, labels=status_counts.index.tolist(), autopct="%1.1f%%")
    st.pyplot(fig)

    st.markdown("---")

    # ✅ BAR CHART
    st.subheader("📦 Inventory by Warehouse")

    warehouse_data = inventory_filtered.groupby("warehouse_location")["stock_level"].sum()

    fig2, ax2 = plt.subplots()
    warehouse_data.plot(kind="bar", ax=ax2)
    ax2.set_ylabel("Stock Level")

    st.pyplot(fig2)

    st.markdown("---")

    # ✅ TOP PRODUCTS
    st.subheader("🏆 Top Products")

    top_products = inventory_filtered.sort_values(
        by="stock_level", ascending=False
    ).head(5)

    st.dataframe(top_products)

    st.markdown("---")

    # ✅ RAW DATA
    with st.expander("📂 View Data"):
        st.write("### Shipments")
        st.dataframe(shipment_filtered)

        st.write("### Inventory")
        st.dataframe(inventory_filtered)


# ============================================
# 3. SAMPLE QUERIES
# ============================================
elif option == "Sample Queries":

    st.title("💡 Sample Queries")

    queries = [
        "Which shipments are delayed?",
        "Show delivered shipments",
        "Which products have low stock?",
        "Inventory in Chennai",
        "Give shipment summary"
    ]

    for q in queries:
        st.write(f"👉 {q}")


# ============================================
# 4. ABOUT PROJECT
# ============================================
elif option == "About Project":

    st.title("📘 About This Project")

    st.markdown("""
    ### 🚀 C&F AI Data Engineering Project

    ✅ Data Ingestion (CSV, JSON, PDF)  
    ✅ Data Transformation  
    ✅ Vector Database (ChromaDB)  
    ✅ Semantic Search (Sheshat equivalent)  
    ✅ LLM Query System  
    ✅ Interactive Dashboard  

    ### 🧠 Architecture:
    ```
    User → Streamlit UI → Vector DB → Retrieval → Answer
    ```

    ### 💼 Use Cases:
    - Shipment tracking  
    - Inventory monitoring  
    - Business insights  
    """)