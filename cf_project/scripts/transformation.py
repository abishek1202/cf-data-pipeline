# ==============================
# IMPORT LIBRARIES
# ==============================

import pandas as pd
import os
import logging
import re  #used to extract data from text and perform pattern matching.    

# ==============================
# LOGGING SETUP
# ==============================

os.makedirs("logs", exist_ok=True) # Ensures the logs/ folder exists.
os.makedirs("data/processed", exist_ok=True)
            
logging.basicConfig(
    filename='logs/transformation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ==============================
# LOAD DATA (FROM INGESTION OUTPUT)
# ==============================

def load_data():
    try:
        inventory_path = "data/raw/inventory_raw.csv"
        shipment_path = "data/raw/shipment_raw.csv"
        invoice_path = "data/raw/invoice_raw.txt"

        inventory = pd.read_csv(inventory_path)
        shipment = pd.read_csv(shipment_path)

        with open(invoice_path, "r", encoding="utf-8") as f:
            invoice_text = f.read()

        logging.info("All datasets loaded successfully")

        return inventory, shipment, invoice_text

    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame(), ""

# ==============================
# CLEAN DATA
# ==============================

def clean_inventory(df):
    try:
        df = df.dropna() # Removes rows with any missing values (NaN) from the DataFrame.
        df = df.drop_duplicates() # Removes duplicate rows from the DataFrame, keeping the first occurrence.

        logging.info("Inventory cleaned successfully")
        return df

    except Exception as e:
        logging.error(f"Error cleaning inventory: {e}")
        return df


def clean_shipment(df):
    try:
        df = df.dropna() # Removes rows with any missing values (NaN) from the DataFrame.
        df = df.drop_duplicates() # Removes duplicate rows from the DataFrame, keeping the first occurrence.
        
        
        df['dispatch_date'] = pd.to_datetime(df['dispatch_date']) # Converts the 'dispatch_date' column to datetime format.
        df['expected_delivery_date'] = pd.to_datetime(df['expected_delivery_date']) # Converts the 'expected_delivery_date' column to datetime format.
        df['actual_delivery_date'] = pd.to_datetime(df['actual_delivery_date']) # Converts the 'actual_delivery_date' column to datetime format.
    
        logging.info("Shipment cleaned successfully")
        return df

    except Exception as e:
        logging.error(f"Error cleaning shipment: {e}")
        return df

# ==============================
# FEATURE ENGINEERING
# ==============================

def add_inventory_features(df):
    try:

        df['total_value'] = df['stock_level'] * df['unit_price_inr'] # Calculate inventory value
        
        logging.info("Inventory features added")
        return df
        
    except Exception as e:
        logging.error(f"Error adding inventory features: {e}")
        return df

# ==============================
# INVOICE PARSING
# ==============================

def process_invoice(text):
    try:
        invoice_id = re.search(r'INV-\\d+', text)       #re.search() → text la pattern search pannum,  INV-\d+ na meaning: INV- → exact word, \d+ → one or more digits. So it will match patterns like INV-12345.
        grand_total = re.search(r'Grand Total:\\s*(\\d+)', text) # Grand Total: → same text match,\s* → space irundhaalum illainaalum ok,(\d+) → numbers edukkum (group aa capture pannum)

        data = {
            "invoice_id": invoice_id.group() if invoice_id else None,
            "grand_total": int(grand_total.group(1)) if grand_total else 0
        }

        logging.info("Invoice processed successfully")
        return data

    except Exception as e:
        logging.error(f"Error processing invoice: {e}")
        return {}

# ==============================
# ANALYTICS FUNCTIONS
# ==============================

def inventory_analysis(df):
    try:
       summary = df.groupby('product_name')['stock_level'].sum().reset_index()
       print("\n Inventory Summary:\n", summary)

       logging.info("Inventory analysis completed")
       return summary

    except Exception as e:
        logging.error(f"Error in inventory analysis: {e}")
        return pd.DataFrame()


def shipment_analysis(df):
    try:
        # Correct column name
        status_summary = df['shipment_status'].value_counts().reset_index()


        print("\n Shipment Status:\n", status_summary)

        logging.info("Shipment analysis completed")
        return status_summary

    except Exception as e:
        logging.error(f"Error in shipment analysis: {e}")
        return pd.DataFrame()

# ===============================
# PREPARE TEXT FOR LLM / SHESHAT
# ===============================
def prepare_text_data(inventory_df, shipment_df):
    try:
        texts = []

        # Inventory → text
        for _, row in inventory_df.iterrows():
            text = f"""
            Product {row['product_name']} has stock level {row['stock_level']} 
            in warehouse {row['warehouse_location']} with price {row['unit_price_inr']} INR.
            """
            texts.append(text)

        # Shipment → text
        for _, row in shipment_df.iterrows():
            text = f"""
            Shipment {row['shipment_id']} from {row['origin_city']} to {row['destination_city']} 
            is {row['shipment_status']} with cost {row['freight_cost_inr']} INR.
            """
            texts.append(text)

        logging.info("Text data prepared successfully")
        return texts

    except Exception as e:
        logging.error(f"Error preparing text data: {e}")
        return []


# ==============================
# SAVE PROCESSED DATA
# ==============================
def save_processed(inventory_df, shipment_df, invoice_data):

    os.makedirs("data/processed", exist_ok=True)

    inventory_df.to_csv("data/processed/inventory_processed.csv", index=False)
    shipment_df.to_csv("data/processed/shipment_processed.csv", index=False)

    # Save invoice structured data
    pd.DataFrame([invoice_data]).to_csv("data/processed/invoice_processed.csv", index=False)

    logging.info("Final processed data saved")
    print("\n Final data saved successfully")


# ==============================
# MAIN EXECUTION
# ==============================

if __name__ == "__main__":

    print("\n Starting Data Transformation...\n")

    inventory, shipment, invoice_text = load_data()

    # Clean data
    inventory = clean_inventory(inventory)
    shipment = clean_shipment(shipment)

    # Feature engineering
    inventory = add_inventory_features(inventory)

    # Process invoice
    invoice_data = process_invoice(invoice_text)

    # Analytics
    inventory_analysis(inventory)
    shipment_analysis(shipment)
    
    
    # ✅ ADD HERE (TEXT PREPARATION START)
    texts = prepare_text_data(inventory, shipment)

    # ✅ SAVE TEXT FILE
    with open("data/processed/text_data.txt", "w", encoding="utf-8") as f:
      for t in texts:
         f.write(t.strip() + "\n\n")
    logging.info("Text data saved successfully")
    # ✅ TEXT PREPARATION END


    # Save final outputs
    save_processed(inventory, shipment, invoice_data)

    print("\n Data Transformation Completed Successfully")
    logging.info("Transformation completed successfully")