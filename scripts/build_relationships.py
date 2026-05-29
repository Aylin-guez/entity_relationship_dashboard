import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

entities = pd.read_csv(DATA_DIR / "entities.csv")
accounts = pd.read_csv(DATA_DIR / "accounts.csv")
transactions = pd.read_csv(DATA_DIR / "transactions.csv")

# Cuenta -> Entidad
account_entity = accounts.merge(
    entities,
    on="entity_id",
    how="left"
)[["account_id", "entity_id", "entity_name", "entity_type", "risk_level"]]

# Agregar datos del emisor
relationships = transactions.merge(
    account_entity,
    left_on="sender_account_id",
    right_on="account_id",
    how="left"
).rename(columns={
    "entity_id": "sender_entity_id",
    "entity_name": "sender_entity_name",
    "entity_type": "sender_entity_type",
    "risk_level": "sender_risk_level"
}).drop(columns=["account_id"])

# Agregar datos del receptor
relationships = relationships.merge(
    account_entity,
    left_on="receiver_account_id",
    right_on="account_id",
    how="left"
).rename(columns={
    "entity_id": "receiver_entity_id",
    "entity_name": "receiver_entity_name",
    "entity_type": "receiver_entity_type",
    "risk_level": "receiver_risk_level"
}).drop(columns=["account_id"])

# Tabla agregada para visualizaciones de relaciones
relationship_summary = relationships.groupby(
    [
        "sender_entity_id",
        "sender_entity_name",
        "sender_entity_type",
        "sender_risk_level",
        "receiver_entity_id",
        "receiver_entity_name",
        "receiver_entity_type",
        "receiver_risk_level"
    ],
    as_index=False
).agg(
    transaction_count=("transaction_id", "count"),
    total_amount_usd=("amount_usd", "sum"),
    avg_amount_usd=("amount_usd", "mean")
)

relationship_summary["total_amount_usd"] = relationship_summary["total_amount_usd"].round(2)
relationship_summary["avg_amount_usd"] = relationship_summary["avg_amount_usd"].round(2)

relationships.to_csv(DATA_DIR / "transactions_enriched.csv", index=False)
relationship_summary.to_csv(DATA_DIR / "relationships.csv", index=False)

print("✅ Relationship files created successfully.")
print("Created:")
print("- data/transactions_enriched.csv")
print("- data/relationships.csv")