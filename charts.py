# charts.py
# This module draws the graphs using Matplotlib.
# It uses the functions from bill_manager.py to get the numbers,
# then just plots them. Each chart opens in its own window.

import matplotlib.pyplot as plt
import bill_manager


def show_category_bar_chart(bills):
    # bar chart: total amount spent in each category
    summary = bill_manager.get_category_summary(bills)
    if len(summary) == 0:
        print("No bills to show in the chart.")
        return

    categories = []
    totals = []
    for item in summary:
        categories.append(item["category"])
        totals.append(item["total"])

    plt.figure(figsize=(7, 5))
    plt.bar(categories, totals, color="skyblue")
    plt.title("Total Spending by Category")
    plt.xlabel("Category")
    plt.ylabel("Total Amount")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()


def show_monthly_trend_chart(bills, category="All"):
    # line chart: how the total spending changes month by month
    period_totals = bill_manager.get_period_totals(bills, category)
    if len(period_totals) == 0:
        print("No bills to show in the chart.")
        return

    periods = []
    totals = []
    for item in period_totals:
        periods.append(item["billing_period"])
        totals.append(item["total"])

    plt.figure(figsize=(7, 5))
    plt.plot(periods, totals, marker="o", color="green")
    plt.title("Monthly Spending Trend (" + category + ")")
    plt.xlabel("Billing Period")
    plt.ylabel("Total Amount")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def show_paid_unpaid_pie_chart(bills):
    # pie chart: how much has been paid vs how much is still outstanding
    if len(bills) == 0:
        print("No bills to show in the chart.")
        return

    paid_total = 0.0
    unpaid_total = 0.0
    for bill in bills:
        if bill["status"] == "Paid":
            paid_total = paid_total + bill["amount"]
        else:
            unpaid_total = unpaid_total + bill["amount"]

    plt.figure(figsize=(5, 5))
    plt.pie([paid_total, unpaid_total],
            labels=["Paid", "Unpaid / Overdue"],
            autopct="%1.1f%%",
            colors=["lightgreen", "salmon"])
    plt.title("Paid vs Unpaid Amount")
    plt.show()
