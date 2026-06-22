# ==============================
# IMPORT MODULES
# ==============================
import logging
import os
from ingestion import *

from transformation import *

# Logging Configuration

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename='logs/pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',encoding='utf-8',force=True
    
)

# ==============================
# PIPELINE FUNCTION
# ==============================
def run_pipeline():

    print("🚀 Starting Full Pipeline...\n")
    logging.info("Pipeline started")

    # ==============================
    # STEP 1: INGESTION
    # ==============================
    inventory = load_inventory("raw/inventory.csv")
    shipment = load_shipment("raw/shipment.json")
    invoice_text = load_invoice("raw/invoice.pdf")

    if inventory is None or shipment is None:
        print("❌ Error loading data")
        logging.error("Error loading data")
        return

    validate_data(inventory, "Inventory")
    validate_data(shipment, "Shipment")

    save_raw_data(inventory, shipment, invoice_text)
    logging.info("Raw data saved successfully")
    print("✅ Ingestion Completed")
    logging.info("Ingestion completed")

    # ==============================
    # STEP 2: TRANSFORMATION
    # ==============================
    inventory = clean_inventory(inventory)
    shipment = clean_shipment(shipment)

    inventory = add_inventory_features(inventory)
    invoice_data = process_invoice(invoice_text)

    save_processed(inventory, shipment, invoice_data)
    print("✅ Transformation Completed")
    logging.info("Transformation completed")

    # ==============================
    # STEP 3: DATA WAREHOUSE (already done separately)
    # ==============================
    print("✅ Data Warehouse Completed")
    logging.info("Data Warehouse completed")

    print("\n🎉 Pipeline Completed Successfully")
    logging.info("Pipeline completed successfully")


# ==============================
# RUN PIPELINE
# ==============================
if __name__ == "__main__":
    run_pipeline()
