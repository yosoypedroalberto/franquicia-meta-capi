# Bulk partner loader script for Juan and Ana

import csv

PARTNERS = [
    {"name": "Juan", "email": "juan@example.com", "role": "partner"},
    {"name": "Ana", "email": "ana@example.com", "role": "partner"}
]

def bulk_load_partners(filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["name", "email", "role"])
        writer.writeheader()
        for partner in PARTNERS:
            writer.writerow(partner)

if __name__ == "__main__":
    bulk_load_partners("partners.csv")
