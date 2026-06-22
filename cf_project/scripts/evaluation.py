# ============================================
# PERFORMANCE EVALUATION
# ============================================

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import time
import os


# ============================================
# LOAD VECTOR DB
# ============================================
def load_db():
    embedding = HuggingFaceEmbeddings()

    db = Chroma(
        persist_directory="vector_db",
        embedding_function=embedding
    )
    return db


# ============================================
# TEST QUERIES
# ============================================
def run_tests(db):

    queries = [
        "Which shipments are delayed?",
        "Show delivered shipments",
        "Which products have low stock?",
        "Show inventory in Chennai",
        "Give shipment summary"
    ]

    results_data = []

    for query in queries:

        start = time.time()

        results = db.similarity_search(query, k=5)

        end = time.time()

        latency = round(end - start, 3)

        result_text = "\n".join([r.page_content for r in results])

        results_data.append({
            "query": query,
            "latency_seconds": latency,
            "results": result_text
        })

        print("\n==============================")
        print(f"Query: {query}")
        print(f"Latency: {latency} sec")
        print("Results:\n", result_text)

    return results_data


# ============================================
# SAVE REPORT
# ============================================
def save_report(data):

    os.makedirs("data/reports", exist_ok=True)

    with open("data/reports/performance_report.txt", "w", encoding="utf-8") as f:

        for item in data:
            f.write(f"Query: {item['query']}\n")
            f.write(f"Latency: {item['latency_seconds']} sec\n")
            f.write("Results:\n")
            f.write(item["results"] + "\n")
            f.write("\n======================\n\n")

    print("\n✅ Performance report saved")


# ============================================
# MAIN
# ============================================
if __name__ == "__main__":

    print("🚀 Running Performance Evaluation...\n")

    db = load_db()

    data = run_tests(db)

    save_report(data)

    print("\n✅ Evaluation Completed")