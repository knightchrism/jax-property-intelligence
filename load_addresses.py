import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL, text


# ---------------------------------------------------------
# 1. CONFIGURATION
# ---------------------------------------------------------

load_dotenv()

FILE_PATH = (
    r".\data\raw\DCPAO REAL ESTATE PIPE DELIMITED TEXT "
    r"UNCERTIFIED AS OF 09-01-2026.txt"
)

ADDRESS_COLUMNS = [
    "row_type",
    "strap",
    "site_number",
    "site_prefix",
    "site_street",
    "site_type",
    "site_unit",
    "site_city",
    "site_zip",
    "building_number",
]


# ---------------------------------------------------------
# 2. EXTRACT SITE ADDRESSES
# ---------------------------------------------------------

print("Reading site address records...")

records = []
rejected_rows = 0

with open(FILE_PATH, "r", encoding="utf-8", errors="replace") as file:
    for line in file:
        fields = line.rstrip("\r\n").split("|")

        if fields[0] != "00004":
            continue

        if len(fields) != 10:
            rejected_rows += 1
            continue

        records.append(fields)


addresses = pd.DataFrame(records, columns=ADDRESS_COLUMNS)

print("Address records extracted:", len(addresses))
print("Malformed address records:", rejected_rows)


# ---------------------------------------------------------
# 3. CLEAN DATA
# ---------------------------------------------------------

print("Cleaning address fields...")

addresses = addresses.drop(columns=["row_type"])

for column in addresses.columns:
    addresses[column] = addresses[column].str.strip()

# Convert empty strings into database NULL values.
addresses = addresses.replace("", None)


# ---------------------------------------------------------
# 4. DATA QUALITY CHECKS
# ---------------------------------------------------------

print("\nQA Checks")
print("----------------------")

print("Total records:", len(addresses))
print("Missing STRAP:", addresses["strap"].isna().sum())
print("Duplicate STRAP:", addresses["strap"].duplicated().sum())

print("\nFirst 5 records:")
print(addresses.head())


# ---------------------------------------------------------
# 5. CONNECT TO POSTGRESQL
# ---------------------------------------------------------

database_url = URL.create(
    "postgresql+psycopg",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME"),
)

engine = create_engine(database_url)


# ---------------------------------------------------------
# 6. CHECK EXISTING DATABASE RECORDS
# ---------------------------------------------------------

with engine.connect() as connection:
    existing_count = connection.execute(
        text("SELECT COUNT(*) FROM property_addresses")
    ).scalar_one()

if existing_count != 0:
    raise RuntimeError(
        f"property_addresses already contains {existing_count} rows. "
        "Load cancelled to prevent duplicate records."
    )


# ---------------------------------------------------------
# 7. LOAD ADDRESSES
# ---------------------------------------------------------

print("\nLoading addresses into PostgreSQL...")

addresses.to_sql(
    name="property_addresses",
    con=engine,
    if_exists="append",
    index=False,
    chunksize=1000,
)

print("Address load complete.")


# ---------------------------------------------------------
# 8. VERIFY LOAD
# ---------------------------------------------------------

with engine.connect() as connection:
    loaded_count = connection.execute(
        text("SELECT COUNT(*) FROM property_addresses")
    ).scalar_one()

print("\nETL Summary")
print("----------------------")
print("Source address records:", len(addresses))
print("Database address records:", loaded_count)
print("Counts match:", loaded_count == len(addresses))
print("ETL complete.")

engine.dispose()
