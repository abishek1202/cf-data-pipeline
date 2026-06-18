# ==============================
# IMPORT MODULES
# ==============================

from ingestion import (
    load_inventory,
    load_shipment,
    load_invoice,
    save_raw_data,
    validate_data
)

from transformation import (
    clean_inventory,
    clean_shipment,
    add_inventory_features,
    process_invoice,
    save_processed
)




# ==============================
# PIPELINE FUNCTION
# ==============================
def run_pipeline():

    print("🚀 Starting Full Pipeline...\n")

    # ==============================
    # STEP 1: INGESTION
    # ==============================
    inventory = load_inventory("raw/inventory.csv")
    shipment = load_shipment("raw/shipment.json")
    invoice_text = load_invoice("raw/invoice.pdf")

    if inventory is None or shipment is None:
        print("❌ Error loading data")
        return

    validate_data(inventory, "Inventory")
    validate_data(shipment, "Shipment")

    save_raw_data(inventory, shipment, invoice_text)
    print("✅ Ingestion Completed")

    # ==============================
    # STEP 2: TRANSFORMATION
    # ==============================
    inventory = clean_inventory(inventory)
    shipment = clean_shipment(shipment)

    inventory = add_inventory_features(inventory)
    invoice_data = process_invoice(invoice_text)

    save_processed(inventory, shipment, invoice_data)
    print("✅ Transformation Completed")

    # ==============================
    # STEP 3: DATA WAREHOUSE (already done separately)
    # ==============================
    print("✅ Data Warehouse Completed")

    print("\n🎉 Pipeline Completed Successfully")


# ==============================
# RUN PIPELINE
# ==============================
if __name__ == "__main__":
    run_pipeline()
