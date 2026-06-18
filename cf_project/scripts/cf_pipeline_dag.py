# =========================================
# IMPORTS
# =========================================
from airflow import DAG

# Import PythonOperator with compatibility for different Airflow versions
import importlib
from typing import Any, TYPE_CHECKING

# Help type-checkers without forcing runtime import of older module names
if TYPE_CHECKING:
    # type: ignore - these are only for static type checkers
    from airflow.operators.python import PythonOperator  # type: ignore

PythonOperator: Any = None
try:
    # Airflow 2.x
    mod = importlib.import_module("airflow.operators.python")
    PythonOperator = getattr(mod, "PythonOperator")
except ImportError:
    # Fallback for older Airflow (<2.0)
    mod = importlib.import_module("airflow.operators.python_operator")
    PythonOperator = getattr(mod, "PythonOperator")

from datetime import datetime

import sys
import os

# ✅ Add your scripts folder inside Docker
sys.path.append('/opt/airflow/scripts')

# ✅ Import your modules (same as your pipeline.py)
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


# =========================================
# TASK 1: INGESTION
# =========================================
def ingestion_task():

    print("🚀 Starting Ingestion...")

    inventory = load_inventory("/opt/airflow/scripts/data/raw/inventory.csv")
    shipment = load_shipment("/opt/airflow/scripts/data/raw/shipment.json")
    invoice_text = load_invoice("/opt/airflow/scripts/data/raw/invoice.pdf")

    if inventory is None or shipment is None:
        raise Exception("❌ Error loading data")

    validate_data(inventory, "Inventory")
    validate_data(shipment, "Shipment")

    save_raw_data(inventory, shipment, invoice_text)

    print("✅ Ingestion Completed")


# =========================================
# TASK 2: TRANSFORMATION
# =========================================
def transformation_task():

    print("🔄 Starting Transformation...")

    import pandas as pd

    # Load processed data (from ingestion output)
    inventory = pd.read_csv("/opt/airflow/scripts/data/processed/inventory_processed.csv")
    shipment = pd.read_csv("/opt/airflow/scripts/data/processed/shipment_processed.csv")

    with open("/opt/airflow/scripts/data/processed/invoice_processed.txt", "r") as f:
        invoice_text = f.read()

    inventory = clean_inventory(inventory)
    shipment = clean_shipment(shipment)

    inventory = add_inventory_features(inventory)
    invoice_data = process_invoice(invoice_text)

    save_processed(inventory, shipment, invoice_data)

    print("✅ Transformation Completed")


# =========================================
# TASK 3: (OPTIONAL LOADING STEP)
# =========================================
def warehouse_task():

    print("✅ Data Warehouse Completed (Handled separately)")


# =========================================
# DAG CONFIGURATION
# =========================================
default_args = {
    "owner": "abishek",
    "start_date": datetime(2024, 1, 1),
    "retries": 1
}

with DAG(
    dag_id="cf_data_pipeline",
    default_args=default_args,
    schedule="@daily",   # ✅ FIXED
    catchup=False
) as dag:

    t1 = PythonOperator(
        task_id="ingestion_task",
        python_callable=ingestion_task
    )

    t2 = PythonOperator(
        task_id="transformation_task",
        python_callable=transformation_task
    )

    t3 = PythonOperator(
        task_id="warehouse_task",
        python_callable=warehouse_task
    )

    # ✅ IMPORTANT (TASK ORDER)
    t1 >> t2 >> t3
    
    
print("✅ DAG Created Successfully")