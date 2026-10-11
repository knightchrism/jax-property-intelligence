import pandas as pd


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
    "building_number"
]


records = []


print("Reading type 00004 site address records...")


with open(FILE_PATH, "r", encoding="utf-8", errors="replace") as file:
    for line in file:
        fields = line.rstrip("\n").split("|")

        if fields[0] != "00004":
            continue

        if len(fields) != 10:
            print("Unexpected field count:", len(fields))
            continue

        records.append(fields)


addresses = pd.DataFrame(
    records,
    columns=ADDRESS_COLUMNS
)


print("\nAddress records loaded:")
print(len(addresses))

print("\nFirst 10 records:")
print(
    addresses[
        [
            "strap",
            "site_number",
            "site_prefix",
            "site_street",
            "site_type",
            "site_unit",
            "site_city",
            "site_zip"
        ]
    ].head(10)
)

print("\nMissing STRAP values:")
print(addresses["strap"].isna().sum())

print("\nDuplicate STRAP values:")
print(addresses["strap"].duplicated().sum())

print("\nSample duplicate STRAP address records:")
print(
    addresses[addresses["strap"].duplicated(keep=False)]
    [
        [
            "strap",
            "site_number",
            "site_prefix",
            "site_street",
            "site_type",
            "site_unit",
            "site_city",
            "site_zip",
            "building_number"
        ]
    ]
    .head(20)
)
