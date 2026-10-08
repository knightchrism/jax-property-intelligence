from collections import Counter


FILE_PATH = (
    r".\data\raw\DCPAO REAL ESTATE PIPE DELIMITED TEXT "
    r"UNCERTIFIED AS OF 09-01-2026.txt"
)


record_counts = Counter()
sample_00001 = []


with open(FILE_PATH, "r", encoding="utf-8", errors="replace") as file:

    for line in file:
        line = line.rstrip("\n")

        if not line:
            continue

        fields = line.split("|")

        record_type = fields[0]

        record_counts[record_type] += 1

        if record_type == "00001" and len(sample_00001) < 5:
            sample_00001.append(fields)


print("Record type counts:")
print("-------------------")

for record_type, count in record_counts.most_common():
    print(record_type, count)


print("\nFirst 5 type 00001 records:")
print("--------------------------")

for record in sample_00001:
    print(record)
