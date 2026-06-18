import pandas as pd

def load_data():
    inventory = pd.read_csv("data/processed/inventory_processed.csv")
    shipment = pd.read_csv("data/processed/shipment_processed.csv")
    invoice = pd.read_csv("data/processed/invoice_processed.csv")
    
    return inventory, shipment, invoice


def convert_to_text(inventory, shipment, invoice):

    documents = []

    # Inventory
    for _, row in inventory.iterrows():
        text = f"Item {row['item_name']} has quantity {row['quantity']} with total value {row['total_value']}"
        documents.append(text)

    # Shipment
    for _, row in shipment.iterrows():
        text = f"Shipment {row['shipment_id']} is {row['status']} from {row['origin']} to {row['destination']}"
        documents.append(text)

    # Invoice
    for _, row in invoice.iterrows():
        text = f"Invoice {row['invoice_id']} has total {row['grand_total']}"
        documents.append(text)

    return documents


if __name__ == "__main__":

    inventory, shipment, invoice = load_data()
    documents = convert_to_text(inventory, shipment, invoice)

    for doc in documents[:5]:
        print(doc)
