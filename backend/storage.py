import csv


def save_to_csv(colleges, filename="data/college_results.csv"):
    if not colleges:
        return

    fieldnames = colleges[0].keys()

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(colleges)