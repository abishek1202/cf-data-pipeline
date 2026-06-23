

#  C&F AI Data Engineering Project

 An end-to-end AI-powered data engineering system for Clearing & Forwarding (C&F) operations.  
This project integrates ETL pipelines, vector databases, and AI-based query systems with a Streamlit UI.

---

##  Project Overview

This system processes multi-format logistics data (inventory, shipment, invoice), builds a searchable knowledge base, and enables natural language querying using AI.

---

##  ABSTRACT

This project presents an end-to-end AI-powered data engineering system designed for Clearing & Forwarding operations.  
It integrates ETL pipelines, vector databases, and AI-based retrieval mechanisms to process logistics data and enable intelligent querying.  

The system supports multi-format data (CSV, JSON, PDF) and transforms it into a structured, searchable, and AI-ready knowledge base.

---

##  INTRODUCTION

The objective of this project is to build a scalable and modular data pipeline for logistics data processing.  
Using modern AI techniques like vector search and retrieval-based querying (RAG), the system enables users to interact with data using natural language.

The solution simplifies data access and provides business insights through an interactive interface.

---
##  Key Features

✅ Multi-format Data Ingestion (CSV, JSON, PDF)  
✅ Data Cleaning & Transformation (ETL Pipeline)  
✅ Vector Database (ChromaDB - Sheshat equivalent)  
✅ Semantic Search & Retrieval  
✅ AI Query System (RAG - Retrieval Augmented Generation)  
✅ Streamlit Web UI  
✅ Interactive Dashboard  
✅ Performance Evaluation & Optimization  

---

---

##  SYSTEM ARCHITECTURE

Raw Data
↓
Data Ingestion (CSV / JSON / PDF)
↓
Data Transformation (Cleaning + Feature Engineering)
↓
Text Conversion (text_data.txt)
↓
Vector Database (ChromaDB)
↓
Retrieval System (Similarity Search)
↓
LLM / Rule-Based Answer Generation
↓
Streamlit User Interface

## 🛠️ TOOLS & TECHNOLOGIES

- Python
- Pandas
- LangChain (Community)
- ChromaDB (Vector Database)
- HuggingFace Embeddings
- Streamlit (UI)
- Matplotlib (Visualization)

---

##  DATASET DESCRIPTION

| Dataset | Format | Description |
|--------|--------|------------|
| Inventory | CSV | Product stock and warehouse data |
| Shipment | JSON | Shipment tracking details |
| Invoice | PDF | Billing and transaction records |

 File Locations:

raw/
data/raw/
data/processed/
vector_db/
scripts/

---

##  PROJECT WORKFLOW

### 1.Data Ingestion
- Reads CSV, JSON, and PDF files
- Converts PDF → text
- Stores cleaned raw files

### 2.Data Transformation
- Removes nulls and duplicates
- Converts data types
- Performs feature engineering (`total_value`)
- Generates `text_data.txt`

### 3.Text Preparation
- Converts structured data into readable sentences
- Example:

Shipment IND-SHP001 from Chennai to Pune is Delayed

### 4.Vector Database Creation
- Converts text into embeddings
- Stores in ChromaDB (`vector_db/`)

### 5.Retrieval System
- Uses similarity search (top-k)
- Retrieves relevant records

### 6.AI Query System
- Accepts user query
- Retrieves relevant data
- Generates answer using rule-based logic

### 7.Streamlit UI
- Input query box
- Displays answer
- Shows retrieved data (debug)

### 8.Performance Evaluation
- Measures latency
- Evaluates retrieval accuracy
- Generates report

---

##  PROJECT STRUCTURE


cf_project/
│
├── raw/
│   ├── inventory.csv
│   ├── shipment.json
│   ├── invoice.pdf
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── reports/
│
├── scripts/
│   ├── ingestion.py
│   ├── transformation.py
│   ├── sheshat_setup.py
│   ├── llm_query.py
│   ├── evaluation.py
│   ├── app.py
│
├── vector_db/
└── logs/

---

##  HOW TO RUN

```bash
python scripts/ingestion.py
python scripts/transformation.py
python scripts/sheshat_setup.py
streamlit run scripts/app.py 


💬 SAMPLE QUERIES
Which shipments are delayed?
Show delivered shipments
Which products have low stock?
Inventory in Chennai
Give shipment summary




