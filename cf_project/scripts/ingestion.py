import json
import pandas as pd
import logging
from PyPDF2 import PdfReader  #Imports PdfReader to extract text from PDF files.

# ==============================
# Logging Configuration
# ==============================
logging.basicConfig(
    filename='logs/ingestion.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ==============================
# Load CSV (Inventory)
# ==============================

def load_inventory(file_path):
    try:
        df = pd.read_csv(file_path)
        logging.info("Inventory CSV loaded successfully")
        return df
    except Exception as e:
        logging.error(f"Error loading inventory CSV: {e}")
        return None


# ==============================
# Load JSON (Shipment)
# ==============================

def load_shipment(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f) # Loads JSON into Python object.

        df = pd.DataFrame(data) #Converts JSON to DataFrame.
        logging.info("Shipment JSON loaded successfully")
        return df

    except Exception as e:
        logging.error(f"Error loading shipment JSON: {e}")
        return None


# ==============================
# Load PDF (Invoice)
# ==============================

def load_invoice(file_path):
    try:
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text() #Extracts text from each extract_text() page and concatenates text += it into a single string.

        logging.info("Invoice PDF loaded successfully")
        return text

    except Exception as e:
        logging.error(f"Error loading invoice PDF: {e}")
        return None


# ==============================
# Save Raw Data
# ==============================

def save_raw_data(inventory_df, shipment_df, invoice_text):
    try:
        # Save inventory
        if inventory_df is not None: #checks if inventory exists.
            inventory_df.to_csv("data/raw/inventory_raw.csv", index=False)

        # Save shipment
        if shipment_df is not None:
            shipment_df.to_csv("data/raw/shipment_raw.csv", index=False)

        # Save invoice text
        if invoice_text is not None:
            with open("data/raw/invoice_raw.txt", "w", encoding="utf-8") as f:
                f.write(invoice_text)

        logging.info("All raw data saved successfully")

    except Exception as e:
        logging.error(f"Error saving raw data: {e}")

# ==============================
# Validate Data
# ==============================

def validate_data(df, name):
    try:
        print(f"\n Validation Report: {name}")
        print("Null Values:\n", df.isnull().sum())
        print("\nData Types:\n", df.dtypes)

        logging.info(f"{name} validation completed")

    except Exception as e:
        logging.error(f"Error validating {name}: {e}")
print(" Starting Data Ingestion Pipeline...")

# ==============================
# Run Ingestion Pipeline
# ==============================

if __name__ == "__main__":

    # File paths
    inventory_path = "c:\\cf_project\\raw\\inventory.csv"
    shipment_path = "c:\\cf_project\\raw\\shipment.json"
    invoice_path = "c:\\cf_project\\raw\\invoice.pdf"

    # Load data
    inventory_df = load_inventory(inventory_path)
    shipment_df = load_shipment(shipment_path)
    invoice_text = load_invoice(invoice_path)

    # Preview
    if inventory_df is not None:
        print("\n Inventory Preview")
        print(inventory_df.head())

    if shipment_df is not None:
        print("\n Shipment Preview")
        print(shipment_df.head())

    if invoice_text is not None:
        print("\n Invoice Preview")
        print(invoice_text[:500])   # show part of text

    # Validate
    if inventory_df is not None:
        validate_data(inventory_df, "Inventory")

    if shipment_df is not None:
        validate_data(shipment_df, "Shipment")

    # Save raw data
    save_raw_data(inventory_df, shipment_df, invoice_text)

    print("\n Data Ingestion Completed Successfully")
