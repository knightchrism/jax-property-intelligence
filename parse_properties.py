import pandas as pd


FILE_PATH = (
    r".\data\raw\DCPAO REAL ESTATE PIPE DELIMITED TEXT "
    r"UNCERTIFIED AS OF 09-01-2026.txt"
)


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


records = []


print("Reading type 00001 property records...")


with open(FILE_PATH, "r", encoding="utf-8", errors="replace") as file:

    for line in file:
        fields = line.rstrip("\n").split("|")

        if fields[0] != "00001":
            continue

        if len(fields) != 31:
            print("Unexpected field count:", len(fields))
            continue

        records.append(fields)


properties = pd.DataFrame(
    records,
    columns=PROPERTY_COLUMNS
)


print("\nProperty records loaded:")
print(len(properties))

print("\nColumns:")
print(properties.columns.tolist())

print("\nFirst 5 records:")
print(
    properties[
        [
            "strap",
            "property_use_code",
            "total_market_value",
            "assessed_value",
            "building_value",
            "documented_acres"
        ]
    ].head()
)

print("\nMissing STRAP values:")
print(properties["strap"].isna().sum())

print("\nDuplicate STRAP values:")
print(properties["strap"].duplicated().sum())
