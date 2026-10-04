# bill_manager.py
# This module has all the logic for working with bills:
# checking the data is valid, adding/updating/deleting/searching bills,
# and calculating totals, averages, comparisons and unusual increases.

from datetime import datetime
import numpy as np
import pandas as pd

CATEGORY_LIST = ["Electricity", "Water", "Internet", "Mobile", "Gas", "Rent", "Other"]
STATUS_LIST = ["Paid", "Unpaid", "Overdue"]

# ---------------------------------------------------------
# Validation functions
# These check the data typed by the user and raise ValueError
# with a simple message if something is wrong.
# ---------------------------------------------------------

def check_amount(value):
    text = value.strip()
    if text == "":
        raise ValueError("Amount cannot be empty.")
    try:
        amount = float(text)
    except ValueError:
        raise ValueError("Amount must be a number.")
    if amount <= 0:
        raise ValueError("Amount must be greater than 0.")
    return round(amount, 2)


def check_date(value, field_name, allow_empty=False):
    text = value.strip()
    if text == "":
        if allow_empty:
            return ""
        raise ValueError(field_name + " cannot be empty.")
    try:
        datetime.strptime(text, "%Y-%m-%d")
    except ValueError:
        raise ValueError(field_name + " must be in YYYY-MM-DD format.")
    return text


def check_period(value):
    text = value.strip()
    if text == "":
        raise ValueError("Billing period cannot be empty.")
    try:
        datetime.strptime(text, "%Y-%m")
    except ValueError:
        raise ValueError("Billing period must be in YYYY-MM format.")
    return text


def check_category(value):
    text = value.strip()
    for item in CATEGORY_LIST:
        if item.lower() == text.lower():
            return item
    raise ValueError("Category must be one of: " + ", ".join(CATEGORY_LIST))


def check_status(value):
    text = value.strip()
    for item in STATUS_LIST:
        if item.lower() == text.lower():
            return item
    raise ValueError("Status must be one of: " + ", ".join(STATUS_LIST))


def check_name(value):
    text = value.strip()
    if text == "":
        raise ValueError("Bill name cannot be empty.")
    return text


# ---------------------------------------------------------
# Add / Update / Delete / Search
# ---------------------------------------------------------

def get_next_id(bills):
    if len(bills) == 0:
        return 1
    max_id = 0
    for bill in bills:
        if bill["id"] > max_id:
            max_id = bill["id"]
    return max_id + 1


def add_bill(bills, name, category, amount, billing_period, due_date, status, paid_date="", notes=""):
    clean_name = check_name(name)
    clean_category = check_category(category)
    clean_amount = check_amount(amount)
    clean_period = check_period(billing_period)
    clean_due_date = check_date(due_date, "Due date")
    clean_status = check_status(status)
    clean_paid_date = check_date(paid_date, "Paid date", allow_empty=True)

    if clean_status == "Paid" and clean_paid_date == "":
        raise ValueError("Please enter a paid date since the status is Paid.")

    new_bill = {
        "id": get_next_id(bills),
        "name": clean_name,
        "category": clean_category,
        "amount": clean_amount,
        "billing_period": clean_period,
        "due_date": clean_due_date,
        "status": clean_status,
        "paid_date": clean_paid_date,
        "notes": notes.strip(),
    }
    bills.append(new_bill)
    return new_bill


def update_bill(bills, bill_id, name, category, amount, billing_period, due_date, status, paid_date="", notes=""):
    clean_name = check_name(name)
    clean_category = check_category(category)
    clean_amount = check_amount(amount)
    clean_period = check_period(billing_period)
    clean_due_date = check_date(due_date, "Due date")
    clean_status = check_status(status)
    clean_paid_date = check_date(paid_date, "Paid date", allow_empty=True)

    if clean_status == "Paid" and clean_paid_date == "":
        raise ValueError("Please enter a paid date since the status is Paid.")

    found = False
    for bill in bills:
        if bill["id"] == bill_id:
            bill["name"] = clean_name
            bill["category"] = clean_category
            bill["amount"] = clean_amount
            bill["billing_period"] = clean_period
            bill["due_date"] = clean_due_date
            bill["status"] = clean_status
            bill["paid_date"] = clean_paid_date
            bill["notes"] = notes.strip()
            found = True

    if not found:
        raise ValueError("No bill found with id " + str(bill_id))


def delete_bill(bills, bill_id):
    found = False
    for i in range(len(bills)):
        if bills[i]["id"] == bill_id:
            bills.pop(i)
            found = True
            break

    if not found:
        raise ValueError("No bill found with id " + str(bill_id))


def search_bills(bills, name="", category="All", status="All"):
    # returns only the bills that match the filters
    # leave name empty or category/status as "All" to skip that filter
    results = []
    for bill in bills:
        if name != "" and name.lower() not in bill["name"].lower():
            continue
        if category != "All" and bill["category"] != category:
            continue
        if status != "All" and bill["status"] != status:
            continue
        results.append(bill)
    return results


# ---------------------------------------------------------
# Totals, averages and comparisons
# ---------------------------------------------------------

def calculate_total(bills):
    # adds up the amount of every bill using a numpy array
    if len(bills) == 0:
        return 0.0
    amount_list = []
    for bill in bills:
        amount_list.append(bill["amount"])
    amount_array = np.array(amount_list)
    return float(np.sum(amount_array))


def calculate_average(bills):
    # finds the average bill amount using a numpy array
    if len(bills) == 0:
        return 0.0
    amount_list = []
    for bill in bills:
        amount_list.append(bill["amount"])
    amount_array = np.array(amount_list)
    return float(np.mean(amount_array))


def get_category_summary(bills):
    # returns total, average and count of bills for each category
    # a pandas table (DataFrame) is used to pick out the rows for
    # each category and add up their amount
    if len(bills) == 0:
        return []

    data_frame = pd.DataFrame(bills)

    category_list = []
    for bill in bills:
        if bill["category"] not in category_list:
            category_list.append(bill["category"])

    summary = []
    for category in category_list:
        rows_for_category = data_frame[data_frame["category"] == category]
        total = rows_for_category["amount"].sum()
        average = rows_for_category["amount"].mean()
        count = len(rows_for_category)
        summary.append({
            "category": category,
            "total": float(total),
            "average": float(average),
            "count": count,
        })
    return summary


def get_period_totals(bills, category="All"):
    # returns the total amount spent in every billing period
    # if a category is given, only that category is used
    filtered = []
    for bill in bills:
        if category == "All" or bill["category"] == category:
            filtered.append(bill)

    if len(filtered) == 0:
        return []

    data_frame = pd.DataFrame(filtered)

    period_list = []
    for bill in filtered:
        if bill["billing_period"] not in period_list:
            period_list.append(bill["billing_period"])
    period_list.sort()

    result = []
    for period in period_list:
        rows_for_period = data_frame[data_frame["billing_period"] == period]
        total = rows_for_period["amount"].sum()
        result.append({"billing_period": period, "total": float(total)})
    return result


def compare_two_periods(bills, period_a, period_b):
    # compares how much was spent per category in two different periods
    category_list = []
    for bill in bills:
        if bill["category"] not in category_list:
            category_list.append(bill["category"])

    comparison = []
    for category in category_list:
        total_a = 0.0
        total_b = 0.0
        for bill in bills:
            if bill["category"] == category and bill["billing_period"] == period_a:
                total_a = total_a + bill["amount"]
            if bill["category"] == category and bill["billing_period"] == period_b:
                total_b = total_b + bill["amount"]
        change = total_b - total_a
        comparison.append({
            "category": category,
            "period_a_total": total_a,
            "period_b_total": total_b,
            "change": change,
        })
    return comparison


# ---------------------------------------------------------
# Unusual increase detection
# ---------------------------------------------------------

def find_unusual_increases(bills, percent_limit=20):
    # goes through each category's bill history month by month
    # and flags a period where the amount jumped up a lot compared to normal.
    #
    # A period is flagged if:
    #   1) it is more than percent_limit percent higher than the previous period, OR
    #   2) it is much higher than the category's usual average so far
    #      (more than 1.5 standard deviations above the mean)

    category_list = []
    for bill in bills:
        if bill["category"] not in category_list:
            category_list.append(bill["category"])

    flagged_list = []

    for category in category_list:
        # collect this category's bills grouped by period into a dictionary
        period_totals = {}
        for bill in bills:
            if bill["category"] == category:
                period = bill["billing_period"]
                if period in period_totals:
                    period_totals[period] = period_totals[period] + bill["amount"]
                else:
                    period_totals[period] = bill["amount"]

        periods = sorted(period_totals.keys())
        if len(periods) < 3:
            continue  # not enough history for this category yet

        amount_list = []
        for period in periods:
            amount_list.append(period_totals[period])
        amount_array = np.array(amount_list)

        for i in range(1, len(amount_array)):
            current = amount_array[i]
            previous = amount_array[i - 1]
            history = amount_array[:i]

            average_so_far = np.mean(history)
            std_so_far = np.std(history)

            reason = ""

            if previous > 0:
                percent_change = (current - previous) / previous * 100
                if percent_change >= percent_limit:
                    reason = f"{percent_change:.1f}% higher than the previous period"

            if std_so_far > 0 and current > average_so_far + 1.5 * std_so_far:
                if reason == "":
                    reason = "much higher than its usual average"

            if reason != "":
                flagged_list.append({
                    "category": category,
                    "billing_period": periods[i],
                    "amount": float(current),
                    "reason": reason,
                })

    return flagged_list