# sample_data.py
# Run this file once to fill the bills file with some example data.
# This makes it easier to test the search, totals and charts features
# without typing everything in by hand.
#
# We made the June electricity bill much higher on purpose, so the
# "Unusual Increases" feature has something to find.

import file_handler
import bill_manager

MONTHS = ["2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06"]

# starting amount for each category
BASE_AMOUNT = {
    "Electricity": 1200,
    "Water": 400,
    "Internet": 900,
    "Mobile": 350,
}


def build_sample_bills():
    bills = []

    for month in MONTHS:
        for category in BASE_AMOUNT:
            # normally the bill stays close to its usual base amount
            amount = BASE_AMOUNT[category]

            # make the electricity bill jump up a lot in June on purpose
            if category == "Electricity" and month == "2025-06":
                amount = amount * 1.6

            bill_manager.add_bill(
                bills,
                name=category + " Bill",
                category=category,
                amount=str(amount),
                billing_period=month,
                due_date=month + "-10",
                status="Paid",
                paid_date=month + "-09",
                notes="",
            )

    return bills


if __name__ == "__main__":
    sample_bills = build_sample_bills()
    file_handler.save_bills(sample_bills)
    print("Added " + str(len(sample_bills)) + " sample bills to " + file_handler.FILE_NAME)
