# test_bill_manager.py
# Simple tests to check that our functions are working correctly.
# Run this file directly: python test_bill_manager.py
# If nothing goes wrong, it will print "All tests passed!" at the end.

import bill_manager


def test_add_bill():
    bills = []
    bill_manager.add_bill(bills, "Electricity Jan", "Electricity", "1500",
                           "2025-01", "2025-01-10", "Paid", "2025-01-09")
    assert len(bills) == 1
    assert bills[0]["name"] == "Electricity Jan"
    assert bills[0]["amount"] == 1500.0
    print("test_add_bill passed")


def test_add_bill_rejects_bad_amount():
    bills = []
    got_error = False
    try:
        bill_manager.add_bill(bills, "Bad Bill", "Electricity", "not_a_number",
                               "2025-01", "2025-01-10", "Unpaid")
    except ValueError:
        got_error = True
    assert got_error is True
    assert len(bills) == 0
    print("test_add_bill_rejects_bad_amount passed")


def test_update_bill():
    bills = []
    bill_manager.add_bill(bills, "Mobile Jan", "Mobile", "399",
                           "2025-01", "2025-01-05", "Unpaid")
    bill_manager.update_bill(bills, 1, "Mobile Jan", "Mobile", "399",
                              "2025-01", "2025-01-05", "Paid", "2025-01-04")
    assert bills[0]["status"] == "Paid"
    assert bills[0]["paid_date"] == "2025-01-04"
    print("test_update_bill passed")


def test_delete_bill():
    bills = []
    bill_manager.add_bill(bills, "Water Jan", "Water", "450",
                           "2025-01", "2025-01-05", "Unpaid")
    bill_manager.delete_bill(bills, 1)
    assert len(bills) == 0
    print("test_delete_bill passed")


def test_delete_missing_bill_gives_error():
    bills = []
    got_error = False
    try:
        bill_manager.delete_bill(bills, 999)
    except ValueError:
        got_error = True
    assert got_error is True
    print("test_delete_missing_bill_gives_error passed")


def test_search_bills():
    bills = []
    bill_manager.add_bill(bills, "Electricity Jan", "Electricity", "1500",
                           "2025-01", "2025-01-10", "Paid", "2025-01-09")
    bill_manager.add_bill(bills, "Internet Jan", "Internet", "999",
                           "2025-01", "2025-01-12", "Unpaid")

    results = bill_manager.search_bills(bills, category="Electricity")
    assert len(results) == 1
    assert results[0]["name"] == "Electricity Jan"
    print("test_search_bills passed")


def test_calculate_total_and_average():
    bills = []
    bill_manager.add_bill(bills, "Bill One", "Water", "100",
                           "2025-01", "2025-01-05", "Paid", "2025-01-04")
    bill_manager.add_bill(bills, "Bill Two", "Water", "200",
                           "2025-02", "2025-02-05", "Paid", "2025-02-04")

    total = bill_manager.calculate_total(bills)
    average = bill_manager.calculate_average(bills)
    assert total == 300.0
    assert average == 150.0
    print("test_calculate_total_and_average passed")


def test_find_unusual_increases():
    bills = []
    bill_manager.add_bill(bills, "Elec Jan", "Electricity", "1000",
                           "2025-01", "2025-01-10", "Paid", "2025-01-09")
    bill_manager.add_bill(bills, "Elec Feb", "Electricity", "1050",
                           "2025-02", "2025-02-10", "Paid", "2025-02-09")
    bill_manager.add_bill(bills, "Elec Mar", "Electricity", "2000",
                           "2025-03", "2025-03-10", "Paid", "2025-03-09")

    flagged = bill_manager.find_unusual_increases(bills, percent_limit=20)
    assert len(flagged) == 1
    assert flagged[0]["billing_period"] == "2025-03"
    print("test_find_unusual_increases passed")


if __name__ == "__main__":
    test_add_bill()
    test_add_bill_rejects_bad_amount()
    test_update_bill()
    test_delete_bill()
    test_delete_missing_bill_gives_error()
    test_search_bills()
    test_calculate_total_and_average()
    test_find_unusual_increases()
    print("\nAll tests passed!")
