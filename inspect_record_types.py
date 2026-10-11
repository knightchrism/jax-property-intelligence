FILE_PATH = (
    r".\data\raw\DCPAO REAL ESTATE PIPE DELIMITED TEXT "
    r"UNCERTIFIED AS OF 09-01-2026.txt"
)

samples = {}
MAX_SAMPLES = 3

with open(FILE_PATH, "r", encoding="utf-8", errors="replace") as file:
    for line in file:
        fields = line.rstrip("\n").split("|")

        record_type = fields[0]

        if record_type not in samples:
            samples[record_type] = []

        if len(samples[record_type]) < MAX_SAMPLES:
            samples[record_type].append(fields)

for record_type in sorted(samples):
    print("\n" + "=" * 70)
    print("RECORD TYPE:", record_type)
    print("=" * 70)

    for record in samples[record_type]:
        print(record)
