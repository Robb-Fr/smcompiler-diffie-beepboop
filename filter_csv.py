import csv
from sys import argv

if __name__ == "__main__":
    id = argv[1]
    new_csv = []
    with open(f"{id}.csv", "r") as f:
        reader = csv.reader(f)
        new_csv.append(reader.__next__())
        for row in reader:
            new_row = []
            for i, col in enumerate(row):
                if i == 0:
                    new_row.append(col[38:])
                if i > 0 and i < 6:
                    new_row.append("{:.3f}".format(float(col)))
                if i == 6:
                    new_row.append(col)
            print(new_row)
            new_csv.append(new_row)
    with open(f"new_{id}.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(new_csv)
