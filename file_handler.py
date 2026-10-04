# file_handler.py
# This module takes care of saving bills to a file and loading them back.
# We are using a CSV file so the data stays saved even after we close the program.

import csv
import os

FILE_NAME = "bills.csv"

# these are the columns we will store in the CSV file
COLUMN_NAMES = ["id", "name", "category", "amount", "billing_period",
                "due_date", "status", "paid_date", "notes"]


def create_file_if_missing():
    # if the file does not exist yet, create it and write the header row
    if not os.path.exists(FILE_NAME):
        file = open(FILE_NAME, "w", newline="")
        writer = csv.DictWriter(file, fieldnames=COLUMN_NAMES)
        writer.writeheader()
        file.close()


def load_bills():
    # reads the CSV file and returns a list of bills
    # each bill is stored as a dictionary
    create_file_if_missing()
    bills = []
    try:
        file = open(FILE_NAME, "r", newline="")
        reader = csv.DictReader(file)
        for row in reader:
            try:
                row["id"] = int(row["id"])
                row["amount"] = float(row["amount"])
                bills.append(row)
            except ValueError:
                # skip a row if the id or amount is not a proper number
                continue
        file.close()
    except OSError as error:
        raise IOError("Could not open the bills file: " + str(error))
    return bills


def save_bills(bills):
    # writes the full list of bills back into the CSV file
    create_file_if_missing()
    try:
        file = open(FILE_NAME, "w", newline="")
        writer = csv.DictWriter(file, fieldnames=COLUMN_NAMES)
        writer.writeheader()
        for bill in bills:
            writer.writerow(bill)
        file.close()
    except OSError as error:
        raise IOError("Could not save the bills file: " + str(error))
