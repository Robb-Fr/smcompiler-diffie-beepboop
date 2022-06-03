import csv
from sys import argv

if __name__ == "__main__":
    id = argv[1]
    new_csv = []
    with open(f"{id}_8cores_arm64.csv", "r") as f:
        reader = csv.reader(f)
        headers = reader.__next__()
        headers[0] = f"# {id}"
        new_csv.append(headers)
        for row in reader:
            new_row = []
            for i, col in enumerate(row):
                if i == 0:
                    new_row.append(col.split("_")[-1])
                if i > 0 and i < 6:
                    new_row.append("{:.3f}".format(float(col)))
                if i == 6:
                    new_row.append(col)
            print(new_row)
            new_csv.append(new_row)
    with open(f"new_{id}_8cores_arm64.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(new_csv)
