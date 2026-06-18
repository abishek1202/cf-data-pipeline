
# IMPORT LIBRARIES

import pandas as pd
import os
import logging
import re

# LOGGING SETUP
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename='logs/transformation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# LOAD DATA (FROM INGESTION OUTPUT)
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


# CLEAN DATA
def clean_inventory(df):
    try:
        df = df.dropna()
        df = df.drop_duplicates()
        df['date'] = pd.to_datetime(df['date'])

        logging.info("Inventory cleaned successfully")
        return df

    except Exception as e:
        logging.error(f"Error cleaning inventory: {e}")
        return df


def clean_shipment(df):
    try:
        df = df.dropna()
        df = df.drop_duplicates()
        df['date'] = pd.to_datetime(df['date'])

        logging.info("Shipment cleaned successfully")
        return df

    except Exception as e:
        logging.error(f"Error cleaning shipment: {e}")
        return df


# FEATURE ENGINEERING
def add_inventory_features(df):
    try:
        df['total_value'] = df['quantity'] * df['price']
        logging.info("Inventory features added")
        return df
    except Exception as e:
        logging.error(f"Error adding inventory features: {e}")
        return df


# INVOICE PARSING
def process_invoice(text):
    try:
        invoice_id = re.search(r'INV-\\d+', text)
        grand_total = re.search(r'Grand Total:\\s*(\\d+)', text)

        data = {
            "invoice_id": invoice_id.group() if invoice_id else None,
            "grand_total": int(grand_total.group(1)) if grand_total else 0
        }

        logging.info("Invoice processed successfully")
        return data

    except Exception as e:
        logging.error(f"Error processing invoice: {e}")
        return {}


# ANALYTICS FUNCTIONS
def inventory_analysis(df):
    try:
        summary = df.groupby('item_name')['quantity'].sum().reset_index()
        print("\n Inventory Summary:\n", summary)

        logging.info("Inventory analysis completed")
        return summary

    except Exception as e:
        logging.error(f"Error in inventory analysis: {e}")
        return pd.DataFrame()


def shipment_analysis(df):
    try:
        status_summary = df['status'].value_counts().reset_index()
        status_summary.columns = ['status', 'count']

        print("\n Shipment Status:\n", status_summary)

        logging.info("Shipment analysis completed")
        return status_summary

    except Exception as e:
        logging.error(f"Error in shipment analysis: {e}")
        return pd.DataFrame()


def time_analysis(df):
    try:
        df['hour'] = pd.to_datetime(df['time']).dt.hour
        hourly = df.groupby('hour')['quantity'].sum().reset_index()

        print("\n Time-based Analysis:\n", hourly)

        logging.info("Time-based analysis completed")
        return hourly

    except Exception as e:
        logging.error(f"Error in time analysis: {e}")
        return pd.DataFrame()


# SAVE PROCESSED DATA
def save_processed(inventory_df, shipment_df, invoice_data):

    os.makedirs("data/processed", exist_ok=True)

    inventory_df.to_csv("data/processed/inventory_processed.csv", index=False)
    shipment_df.to_csv("data/processed/shipment_processed.csv", index=False)

    # Save invoice structured data
    pd.DataFrame([invoice_data]).to_csv("data/processed/invoice_processed.csv", index=False)

    logging.info("Final processed data saved")
    print("\n Final data saved successfully")



# MAIN EXECUTION
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
    time_analysis(inventory)

    # Save final outputs
    save_processed(inventory, shipment, invoice_data)

    print("\n Data Transformation Completed Successfully")
    logging.info("Transformation completed successfully")