import csv


def read_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        num = 0
        for row in reader:
            if num > 0:
                yield row
            num += 1
