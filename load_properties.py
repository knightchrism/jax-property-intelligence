import os

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


# ---------------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# ---------------------------------------------------------

load_dotenv()


# ---------------------------------------------------------
# SOURCE FILE
# ---------------------------------------------------------

FILE_PATH = (
    r".\data\raw\DCPAO REAL ESTATE PIPE DELIMITED TEXT "
    r"UNCERTIFIED AS OF 09-01-2026.txt"
)


# ---------------------------------------------------------
# COLUMN DEFINITIONS FOR RECORD TYPE 00001
# ---------------------------------------------------------

PROPERTY_COLUMNS = [
    "row_type",
    "strap",
    "section",
    "township",
    "range",
    "tile_number",
    "confidentiality_flag",
    "mailing_address_1",
    "mailing_address_2",
    "mailing_city",
    "mailing_state",
    "mailing_zip",
    "property_use_code",
    "subdivision_number",
    "subdivision_name",
    "plat_book",
    "plat_page",
    "neighborhood_code",
    "percent_capped",
    "valuation_method",
    "cap_base_year",
    "total_market_value",
    "assessed_value",
    "building_value",
    "total_just_value",
    "school_taxable",
    "county_municipal_taxable",
    "sjrwmd_taxable",
    "taxing_district_code",
    "gis_square_feet",
    "documented_acres"
]


# ---------------------------------------------------------
# READ ONLY TYPE 00001 RECORDS
# ---------------------------------------------------------

records = []

print("Reading property records...")

with open(FILE_PATH, "r", encoding="utf-8", errors="replace") as file:
    for line in file:
        fields = line.rstrip("\n").split("|")

        if fields[0] != "00001":
            continue

        if len(fields) != 31:
            continue

        records.append(fields)


properties = pd.DataFrame(
    records,
    columns=PROPERTY_COLUMNS
)

print("Records read:", len(properties))


# ---------------------------------------------------------
# CLEAN COLUMN NAMES
# ---------------------------------------------------------

properties = properties.rename(
    columns={
        "range": "range_code"
    }
)

properties = properties.drop(
    columns=["row_type"]
)


# ---------------------------------------------------------
# CONVERT NUMERIC FIELDS
# ---------------------------------------------------------

numeric_columns = [
    "percent_capped",
    "cap_base_year",
    "total_market_value",
    "assessed_value",
    "building_value",
    "total_just_value",
    "school_taxable",
    "county_municipal_taxable",
    "sjrwmd_taxable",
    "gis_square_feet",
    "documented_acres"
]

for column in numeric_columns:
    properties[column] = pd.to_numeric(
        properties[column],
        errors="coerce"
    )


# ---------------------------------------------------------
# QA CHECKS
# ---------------------------------------------------------

print("\nQA checks")
print("---------")

print("Records:", len(properties))

print("Missing STRAP values:")
print(properties["strap"].isna().sum())

print("Duplicate STRAP values:")
print(properties["strap"].duplicated().sum())


# ---------------------------------------------------------
# BUILD DATABASE CONNECTION
# ---------------------------------------------------------

database_url = (
    f"postgresql+psycopg://"
    f"{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(database_url)


# ---------------------------------------------------------
# LOAD INTO POSTGRESQL
# ---------------------------------------------------------

print("\nLoading properties into PostgreSQL...")

properties.to_sql(
    name="properties",
    con=engine,
    if_exists="append",
    index=False,
    method="multi",
    chunksize=1000
)

print("Property load complete.")


# ---------------------------------------------------------
# FINISHED
# ---------------------------------------------------------

print("\nETL complete.")
