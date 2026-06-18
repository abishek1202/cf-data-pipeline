

# IMPORT LIBRARIES

import pandas as pd
from sqlalchemy import create_engine
import logging
import os


# LOGGING CONFIGURATION

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename='logs/load_postgres.log',
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# STEP 1: DATABASE CONNECTION

def create_connection():
    try:
        user = "postgres"
        password = "1234qwer"
        host = "localhost"
        port = "1202"   # ✅ change if yours different
        database = "cf_dw"

        engine = create_engine(
            f"postgresql://{user}:{password}@{host}:{port}/{database}"
        )

        logging.info("PostgreSQL connection created")
        return engine

    except Exception as e:
        logging.error(f"Connection error: {e}")
        return None


# ==============================
# STEP 2: LOAD FINAL DATA
# ==============================
def load_data():
    try:
        inventory = pd.read_csv("data/processed/inventory_processed.csv")
        shipment = pd.read_csv("data/processed/shipment_processed.csv")
        invoice = pd.read_csv("data/processed/invoice_processed.csv")

        logging.info("All final datasets loaded")
        return inventory, shipment, invoice

    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return None, None, None


# ==============================
# STEP 3: FACT TABLES
# ==============================
def create_fact_inventory(df, engine):
    try:
        df.to_sql(
            "fact_inventory",
            engine,
            if_exists="replace",
            index=False
        )
        print("✅ Fact Inventory created")
        logging.info("Fact Inventory table created")

    except Exception as e:
        logging.error(f"Error creating fact_inventory: {e}")


def create_fact_shipment(df, engine):
    try:
        df.to_sql(
            "fact_shipment",
            engine,
            if_exists="replace",
            index=False
        )
        print("✅ Fact Shipment created")
        logging.info("Fact Shipment table created")

    except Exception as e:
        logging.error(f"Error creating fact_shipment: {e}")


def create_fact_invoice(df, engine):
    try:
        df.to_sql(
            "fact_invoice",
            engine,
            if_exists="replace",
            index=False
        )
        print("✅ Fact Invoice created")
        logging.info("Fact Invoice table created")

    except Exception as e:
        logging.error(f"Error creating fact_invoice: {e}")


# ==============================
# STEP 4: DIMENSION TABLES
# ==============================
def create_dim_item(df, engine):
    try:
        dim = df[['item_name']].drop_duplicates()

        dim.to_sql(
            "dim_item",
            engine,
            if_exists="replace",
            index=False
        )

        print("✅ Dimension: Item created")
        logging.info("Dimension item created")

    except Exception as e:
        logging.error(f"Error creating dim_item: {e}")


def create_dim_location(df, engine):
    try:
        dim = df[['warehouse']].drop_duplicates()

        dim.to_sql(
            "dim_location",
            engine,
            if_exists="replace",
            index=False
        )

        print("✅ Dimension: Location created")
        logging.info("Dimension location created")

    except Exception as e:
        logging.error(f"Error creating dim_location: {e}")


def create_dim_status(df, engine):
    try:
        dim = df[['status']].drop_duplicates()

        dim.to_sql(
            "dim_status",
            engine,
            if_exists="replace",
            index=False
        )

        print("✅ Dimension: Status created")
        logging.info("Dimension status created")

    except Exception as e:
        logging.error(f"Error creating dim_status: {e}")


# ==============================
# STEP 5: RUN ANALYTICS QUERIES
# ==============================
def run_queries(engine):
    try:
        print("\n📊 Running Queries...\n")

        # Inventory total value
        query1 = """
        SELECT item_name, SUM(total_value) AS total_value
        FROM fact_inventory
        GROUP BY item_name;
        """
        print("📦 Inventory Value:\n", pd.read_sql(query1, engine))

        # Shipment count by status
        query2 = """
        SELECT status, COUNT(*) AS count
        FROM fact_shipment
        GROUP BY status;
        """
        print("\n🚚 Shipment Status:\n", pd.read_sql(query2, engine))

        # Invoice total
        query3 = """
        SELECT SUM(grand_total) AS total_revenue
        FROM fact_invoice;
        """
        print("\n💰 Total Revenue:\n", pd.read_sql(query3, engine))

        logging.info("Queries executed successfully")

    except Exception as e:
        logging.error(f"Query error: {e}")


# ==============================
# STEP 6: MAIN EXECUTION
# ==============================
if __name__ == "__main__":

    print("\n🚀 Loading data into PostgreSQL...\n")
    logging.info("Starting DB load process")

    engine = create_connection()

    inventory, shipment, invoice = load_data()

    # Fact tables
    create_fact_inventory(inventory, engine)
    create_fact_shipment(shipment, engine)
    create_fact_invoice(invoice, engine)

    # Dimension tables
    create_dim_item(inventory, engine)
    create_dim_location(inventory, engine)
    create_dim_status(shipment, engine)

    # Run queries
    run_queries(engine)

    print("\n✅ Data successfully loaded into PostgreSQL")
    logging.info("Load process completed")