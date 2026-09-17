import pandas as pd
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# CONFIGURATION
# ============================================================

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

CSV_PATH = "data/processed/processed_supply_chain.csv"

BATCH_SIZE = 2000


# ============================================================
# CONNECT TO DATABASE
# ============================================================

print("=" * 60)
print("SUPPLY CHAIN DATA LOADER")
print("=" * 60)

print("\nConnecting to MySQL...")

connection = pymysql.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    cursorclass=pymysql.cursors.Cursor
)

print("MySQL connection successful!")


# ============================================================
# LOAD CSV
# ============================================================

print("\nLoading processed dataset...")

df = pd.read_csv(CSV_PATH)

print(f"Rows found: {len(df):,}")


# ============================================================
# PREPARE DATA
# ============================================================

print("\nPreparing data...")

# Convert dates

df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)

df["shipping_date"] = pd.to_datetime(
    df["shipping_date"],
    errors="coerce"
)

# Convert NaN to None for MySQL

df = df.where(
    pd.notnull(df),
    None
)


# ============================================================
# SQL INSERT
# ============================================================

columns = list(df.columns)

column_names = ", ".join(
    f"`{column}`"
    for column in columns
)

placeholders = ", ".join(
    ["%s"] * len(columns)
)

insert_query = f"""
INSERT INTO supply_chain_orders
(
    {column_names}
)
VALUES
(
    {placeholders}
)
"""


# ============================================================
# INSERT IN BATCHES
# ============================================================

print("\nStarting data insertion...")

cursor = connection.cursor()

total_rows = len(df)

for start in range(
    0,
    total_rows,
    BATCH_SIZE
):

    end = min(
        start + BATCH_SIZE,
        total_rows
    )

    batch = df.iloc[
        start:end
    ]

    records = [
        tuple(row)
        for row in batch.itertuples(
            index=False,
            name=None
        )
    ]

    cursor.executemany(
        insert_query,
        records
    )

    connection.commit()

    progress = (
        end / total_rows
    ) * 100

    print(
        f"Loaded {end:,}/{total_rows:,} "
        f"({progress:.1f}%)"
    )


# ============================================================
# VERIFY
# ============================================================

print("\nVerifying database...")

cursor.execute(
    "SELECT COUNT(*) FROM supply_chain_orders"
)

count = cursor.fetchone()[0]

print(
    f"Rows in MySQL: {count:,}"
)


# ============================================================
# CLOSE
# ============================================================

cursor.close()

connection.close()

print("\n" + "=" * 60)
print("DATA LOADING COMPLETED")
print("=" * 60)