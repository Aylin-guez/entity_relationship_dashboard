import pandas as pd
import random
from faker import Faker
from pathlib import Path

fake = Faker()
random.seed(42)
Faker.seed(42)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# -------------------------
# ENTITIES
# -------------------------
entity_types = ["Company", "Individual", "Vendor", "Client"]

entities = []
for i in range(1, 41):
    entity_type = random.choice(entity_types)

    if entity_type == "Company":
        name = fake.company()
    else:
        name = fake.name()

    entities.append({
        "entity_id": f"ENT{i:03}",
        "entity_name": name,
        "entity_type": entity_type,
        "risk_level": random.choice(["Low", "Medium", "High"]),
        "country": fake.country()
    })

entities_df = pd.DataFrame(entities)

# -------------------------
# ACCOUNTS
# -------------------------
accounts = []
account_types = ["Bank Account", "Wallet", "Business Account"]

account_counter = 1

for entity in entities:
    number_of_accounts = random.randint(1, 3)

    for _ in range(number_of_accounts):
        accounts.append({
            "account_id": f"ACC{account_counter:04}",
            "entity_id": entity["entity_id"],
            "account_type": random.choice(account_types),
            "created_date": fake.date_between(start_date="-2y", end_date="-6m")
        })
        account_counter += 1

accounts_df = pd.DataFrame(accounts)

# -------------------------
# TRANSACTIONS
# -------------------------
transactions = []
transaction_types = ["Transfer", "Payment", "Refund", "Withdrawal", "Deposit"]

account_ids = accounts_df["account_id"].tolist()

for i in range(1, 501):
    sender = random.choice(account_ids)
    receiver = random.choice(account_ids)

    while receiver == sender:
        receiver = random.choice(account_ids)

    amount = random.randint(25, 15000)

    transactions.append({
        "transaction_id": f"TX{i:05}",
        "sender_account_id": sender,
        "receiver_account_id": receiver,
        "amount_usd": amount,
        "transaction_type": random.choice(transaction_types),
        "transaction_date": fake.date_time_between(start_date="-365d", end_date="now"),
        "status": random.choice(["Completed", "Completed", "Completed", "Pending", "Flagged"]),
        "source_system": random.choice(["Bank Export", "Wallet Export", "ERP", "Manual Report"])
    })

transactions_df = pd.DataFrame(transactions)

# -------------------------
# EVENTS
# -------------------------
events = []
event_types = [
    "Account Created",
    "High Value Transaction",
    "Repeated Transfers",
    "Manual Review",
    "Unusual Activity"
]

for i in range(1, 81):
    entity = random.choice(entities)

    events.append({
        "event_id": f"EVT{i:04}",
        "entity_id": entity["entity_id"],
        "event_type": random.choice(event_types),
        "event_date": fake.date_time_between(start_date="-365d", end_date="now"),
        "notes": fake.sentence()
    })

events_df = pd.DataFrame(events)

# -------------------------
# EXPORT
# -------------------------
entities_df.to_csv(DATA_DIR / "entities.csv", index=False)
accounts_df.to_csv(DATA_DIR / "accounts.csv", index=False)
transactions_df.to_csv(DATA_DIR / "transactions.csv", index=False)
events_df.to_csv(DATA_DIR / "events.csv", index=False)

print("✅ Synthetic relationship dataset created successfully.")
print(f"Files saved in: {DATA_DIR}")