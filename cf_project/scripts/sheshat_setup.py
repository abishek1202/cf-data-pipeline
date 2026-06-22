# ===============================
# SHESHAT SETUP (VECTOR DATABASE)
# ===============================

import os
import logging
from langchain_community.embeddings import HuggingFaceEmbeddings # Loads a pretrained embedding model (converts text → numeric vectors
from langchain_community.vectorstores import Chroma #  Imports Chroma vector database, used to store and search embeddings.

# ===============================
# logging setup
# ===============================

   
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename='logs/sheshat_setup.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',encoding='utf-8',force=True
)

# ===============================
# STEP 1: LOAD TEXT DATA
# ===============================

def load_documents():
    try:
        with open("data/processed/text_data.txt", "r", encoding="utf-8") as f: # encoding="utf-8" ensures that the file is read correctly, especially if it contains special characters.
            docs = f.read().split("\n\n") # f.read() reads the entire file as a single string, and then split("\n\n") divides it into a list of documents based on double newlines. Each document is separated by two newline characters, which is a common way to denote the end of one document and the start of another in text files.

        # Remove empty texts
        docs = [d.strip() for d in docs if d.strip()] #  removes spaces front and end for each word, and also " ", also.

        print(f"✅ Loaded {len(docs)} documents")
        logging.info(f"Loaded {len(docs)} documents successfully")
        return docs  # returns the list of documents like  "","".

    except Exception as e:
        print(f"❌ Error loading documents: {e}")
        logging.error(f"Error loading documents: {e}")
        
        return []


# ===============================
# STEP 2: CREATE METADATA ("we create keyword for document to find or get the related data)
# ===============================
def create_metadata(documents):
    texts = []
    metadata = []

    for doc in documents:
        texts.append(doc)

        # Simple classification
        if "Product" in doc:
            metadata.append({"type": "inventory"})
        elif "Shipment" in doc:
            metadata.append({"type": "shipment"})
        else:
            metadata.append({"type": "unknown"})

    return texts, metadata
logging.info("Metadata created successfully")


# ===============================
# STEP 3: CREATE VECTOR DATABASE
# ===============================
def create_vector_db(texts, metadata):
    try:
        print("⚙️ Creating embeddings...")
        logging.info("Creating embeddings for documents")

        embedding = HuggingFaceEmbeddings() # this model converts text into numeric vectors that capture the meaning of the text. understandable numbers for AI module.

        print("⚙️ Creating vector database...")
        logging.info("Creating vector database")
        db = Chroma.from_texts(
            texts=texts,                    # the list of documents we want to store in the vector database.
            embedding=embedding,            # the embedding model we initialized, which will convert the texts into vectors before storing them in the database.
            metadatas=metadata,             # the metadata we created for each document, which will be stored alongside the vectors in the database. This allows us to filter or search based on metadata later.
            persist_directory="vector_db"   # the directory where the vector database will be saved as (name)
        )

        db.persist()

        print("✅ Vector DB created successfully")
        logging.info("Vector DB created successfully")
        
        return db # text--vector, if query, it will find the related vector and return the text.

    except Exception as e:
        print(f"❌ Error creating vector DB: {e}")
        logging.error(f"Error creating vector DB: {e}")
        
        return None


# ===============================
# STEP 4: TEST SEARCH
# ===============================
def test_search(db):
    try:
        print("\n🔍 Testing retrieval...\n")
        logging.info("Testing retrieval")


        query = "Which shipments are delayed?"

        results = db.similarity_search(query, k=3) # in db, it use similarity_search function to find the most similar documents to the query and shows the top 3 results (k=3). 

        for i, r in enumerate(results): # enumerate gives value and index, r is the result, i is the index. it will print the content of the result and its metadata.
            print(f"\nResult {i+1}:")
            print(r.page_content)
            print("Metadata:", r.metadata)

        logging.info("Retrieval completed successfully")
        return results

    except Exception as e:
        print(f"❌ Search error: {e}")
        logging.error(f"Search error: {e}")
        return []


# ===============================
# STEP 5: SAVE RETRIEVAL REPORT
# ===============================
def save_report(results):
    try:
        os.makedirs("data/processed", exist_ok=True)

        with open("data/processed/retrieval_report.txt", "w", encoding="utf-8") as f:
            f.write("QUERY: Which shipments are delayed?\n\n")

            for i, r in enumerate(results):
                f.write(f"Result {i+1}:\n")
                f.write(r.page_content + "\n")
                f.write(f"Metadata: {r.metadata}\n\n")


        print("✅ Retrieval report saved")
        logging.info("Retrieval report saved successfully")

    except Exception as e:
        print(f"❌ Erroutor saving report: {e}")
        logging.error(f"Error saving report: {e}")


# ===============================
# MAIN EXECUTION
# ===============================
if __name__ == "__main__":

    print("\n🚀 Starting Sheshat Setup...\n")
    logging.info("Sheshat setup started")

    # Step 1: Load documents
    documents = load_documents()

    # Step 2: Metadata
    texts, metadata = create_metadata(documents)

    # Step 3: Create DB
    db = create_vector_db(texts, metadata)

    # Step 4: Test search
    if db:
        results = test_search(db)

        # Step 5: Save report
        save_report(results)

    print("\n✅ Sheshat Setup Completed Successfully")
    logging.info("Sheshat setup completed successfully")