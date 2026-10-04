# gui.py
# This module builds the window (GUI) using Tkinter.
# It uses file_handler.py to load/save bills, bill_manager.py to work
# with the bills, and charts.py to show the graphs.
#
# We keep the list of bills and the widgets as simple global variables
# so every function in this file can use them.

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

import file_handler
import bill_manager
import charts

# --- global variables used across this file ---
window = None
bills = []
selected_id = None

entry_name = None
combo_category = None
entry_amount = None
entry_period = None
entry_due_date = None
combo_status = None
entry_paid_date = None
entry_notes = None

search_name = None
search_category = None
search_status = None

table = None


# -----------------------------------------------------
# Top section: form to add/edit a bill
# -----------------------------------------------------
def create_form_section():
    global entry_name, combo_category, entry_amount, entry_period
    global entry_due_date, combo_status, entry_paid_date, entry_notes

    form_frame = ttk.LabelFrame(window, text="Bill Details")
    form_frame.pack(fill="x", padx=10, pady=8)

    ttk.Label(form_frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
    entry_name = ttk.Entry(form_frame, width=18)
    entry_name.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(form_frame, text="Category").grid(row=0, column=2, padx=5, pady=5)
    combo_category = ttk.Combobox(form_frame, values=bill_manager.CATEGORY_LIST,
                                   state="readonly", width=15)
    combo_category.grid(row=0, column=3, padx=5, pady=5)

    ttk.Label(form_frame, text="Amount").grid(row=0, column=4, padx=5, pady=5)
    entry_amount = ttk.Entry(form_frame, width=12)
    entry_amount.grid(row=0, column=5, padx=5, pady=5)

    ttk.Label(form_frame, text="Period (YYYY-MM)").grid(row=1, column=0, padx=5, pady=5)
    entry_period = ttk.Entry(form_frame, width=18)
    entry_period.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(form_frame, text="Due Date (YYYY-MM-DD)").grid(row=1, column=2, padx=5, pady=5)
    entry_due_date = ttk.Entry(form_frame, width=15)
    entry_due_date.grid(row=1, column=3, padx=5, pady=5)

    ttk.Label(form_frame, text="Status").grid(row=1, column=4, padx=5, pady=5)
    combo_status = ttk.Combobox(form_frame, values=bill_manager.STATUS_LIST,
                                 state="readonly", width=12)
    combo_status.grid(row=1, column=5, padx=5, pady=5)

    ttk.Label(form_frame, text="Paid Date (YYYY-MM-DD)").grid(row=2, column=0, padx=5, pady=5)
    entry_paid_date = ttk.Entry(form_frame, width=18)
    entry_paid_date.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(form_frame, text="Notes").grid(row=2, column=2, padx=5, pady=5)
    entry_notes = ttk.Entry(form_frame, width=30)
    entry_notes.grid(row=2, column=3, columnspan=2, padx=5, pady=5)

    button_frame = ttk.Frame(form_frame)
    button_frame.grid(row=3, column=0, columnspan=6, pady=8)

    ttk.Button(button_frame, text="Add Bill", command=add_bill_clicked).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Update Selected", command=update_bill_clicked).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Delete Selected", command=delete_bill_clicked).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Clear Form", command=clear_form).pack(side="left", padx=5)


# -----------------------------------------------------
# Search and filter section
# -----------------------------------------------------
def create_search_section():
    global search_name, search_category, search_status

    search_frame = ttk.LabelFrame(window, text="Search / Filter")
    search_frame.pack(fill="x", padx=10, pady=5)

    ttk.Label(search_frame, text="Name has:").grid(row=0, column=0, padx=5, pady=5)
    search_name = ttk.Entry(search_frame, width=15)
    search_name.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(search_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5)
    search_category = ttk.Combobox(search_frame, values=["All"] + bill_manager.CATEGORY_LIST,
                                    state="readonly", width=14)
    search_category.set("All")
    search_category.grid(row=0, column=3, padx=5, pady=5)

    ttk.Label(search_frame, text="Status:").grid(row=0, column=4, padx=5, pady=5)
    search_status = ttk.Combobox(search_frame, values=["All"] + bill_manager.STATUS_LIST,
                                  state="readonly", width=12)
    search_status.set("All")
    search_status.grid(row=0, column=5, padx=5, pady=5)

    ttk.Button(search_frame, text="Search", command=refresh_table).grid(row=0, column=6, padx=5)
    ttk.Button(search_frame, text="Reset", command=reset_search).grid(row=0, column=7, padx=5)


# -----------------------------------------------------
# Table section: shows the list of bills
# -----------------------------------------------------
def create_table_section():
    global table

    columns = ("id", "name", "category", "amount", "billing_period",
               "due_date", "status", "paid_date", "notes")
    headings = ("ID", "Name", "Category", "Amount", "Period",
                "Due Date", "Status", "Paid Date", "Notes")

    table = ttk.Treeview(window, columns=columns, show="headings", height=12)
    for col, head in zip(columns, headings):
        table.heading(col, text=head)
        table.column(col, width=90, anchor="center")

    table.pack(fill="both", expand=True, padx=10, pady=5)
    table.bind("<<TreeviewSelect>>", row_selected)


# -----------------------------------------------------
# Bottom section: summary, comparison, charts
# -----------------------------------------------------
def create_bottom_buttons():
    bottom_frame = ttk.Frame(window)
    bottom_frame.pack(fill="x", padx=10, pady=8)

    ttk.Button(bottom_frame, text="Show Summary", command=show_summary).pack(side="left", padx=5)
    ttk.Button(bottom_frame, text="Compare Two Periods", command=compare_periods_clicked).pack(side="left", padx=5)
    ttk.Button(bottom_frame, text="Unusual Increases", command=show_unusual_increases).pack(side="left", padx=5)
    ttk.Button(bottom_frame, text="Bar Chart", command=show_bar_chart).pack(side="left", padx=5)
    ttk.Button(bottom_frame, text="Trend Chart", command=show_trend_chart).pack(side="left", padx=5)
    ttk.Button(bottom_frame, text="Pie Chart", command=show_pie_chart).pack(side="left", padx=5)


# -----------------------------------------------------
# Button actions
# -----------------------------------------------------
def add_bill_clicked():
    try:
        bill_manager.add_bill(
            bills,
            entry_name.get(),
            combo_category.get(),
            entry_amount.get(),
            entry_period.get(),
            entry_due_date.get(),
            combo_status.get(),
            entry_paid_date.get(),
            entry_notes.get(),
        )
        file_handler.save_bills(bills)
        clear_form()
        refresh_table()
        messagebox.showinfo("Success", "Bill added.")
    except ValueError as error:
        messagebox.showerror("Invalid Input", str(error))
    except IOError as error:
        messagebox.showerror("File Error", str(error))


def update_bill_clicked():
    if selected_id is None:
        messagebox.showwarning("No Selection", "Please select a bill from the table first.")
        return
    try:
        bill_manager.update_bill(
            bills,
            selected_id,
            entry_name.get(),
            combo_category.get(),
            entry_amount.get(),
            entry_period.get(),
            entry_due_date.get(),
            combo_status.get(),
            entry_paid_date.get(),
            entry_notes.get(),
        )
        file_handler.save_bills(bills)
        clear_form()
        refresh_table()
        messagebox.showinfo("Success", "Bill updated.")
    except ValueError as error:
        messagebox.showerror("Invalid Input", str(error))
    except IOError as error:
        messagebox.showerror("File Error", str(error))


def delete_bill_clicked():
    if selected_id is None:
        messagebox.showwarning("No Selection", "Please select a bill from the table first.")
        return
    answer = messagebox.askyesno("Confirm", "Delete the selected bill?")
    if not answer:
        return
    try:
        bill_manager.delete_bill(bills, selected_id)
        file_handler.save_bills(bills)
        clear_form()
        refresh_table()
    except ValueError as error:
        messagebox.showerror("Error", str(error))
    except IOError as error:
        messagebox.showerror("File Error", str(error))


def row_selected(event):
    global selected_id

    selected = table.selection()
    if len(selected) == 0:
        return
    values = table.item(selected[0], "values")

    selected_id = int(values[0])
    entry_name.delete(0, tk.END)
    entry_name.insert(0, values[1])
    combo_category.set(values[2])
    entry_amount.delete(0, tk.END)
    entry_amount.insert(0, values[3])
    entry_period.delete(0, tk.END)
    entry_period.insert(0, values[4])
    entry_due_date.delete(0, tk.END)
    entry_due_date.insert(0, values[5])
    combo_status.set(values[6])
    entry_paid_date.delete(0, tk.END)
    entry_paid_date.insert(0, values[7])
    entry_notes.delete(0, tk.END)
    entry_notes.insert(0, values[8])


def clear_form():
    global selected_id

    selected_id = None
    entry_name.delete(0, tk.END)
    combo_category.set("")
    entry_amount.delete(0, tk.END)
    entry_period.delete(0, tk.END)
    entry_due_date.delete(0, tk.END)
    combo_status.set("")
    entry_paid_date.delete(0, tk.END)
    entry_notes.delete(0, tk.END)
    for item in table.selection():
        table.selection_remove(item)


def reset_search():
    search_name.delete(0, tk.END)
    search_category.set("All")
    search_status.set("All")
    refresh_table()


def refresh_table():
    for row in table.get_children():
        table.delete(row)

    results = bill_manager.search_bills(
        bills,
        search_name.get(),
        search_category.get(),
        search_status.get(),
    )

    for bill in results:
        table.insert("", "end", values=(
            bill["id"], bill["name"], bill["category"],
            bill["amount"], bill["billing_period"], bill["due_date"],
            bill["status"], bill["paid_date"], bill["notes"],
        ))


# -----------------------------------------------------
# Summary / comparison / unusual increases (shown as message boxes)
# -----------------------------------------------------
def show_summary():
    total = bill_manager.calculate_total(bills)
    average = bill_manager.calculate_average(bills)
    category_summary = bill_manager.get_category_summary(bills)

    message = "Total Spent: " + str(round(total, 2)) + "\n"
    message = message + "Average Bill: " + str(round(average, 2)) + "\n\n"
    message = message + "By Category:\n"
    for item in category_summary:
        message = message + "- " + item["category"] + ": total = " + str(round(item["total"], 2))
        message = message + ", average = " + str(round(item["average"], 2))
        message = message + ", count = " + str(item["count"]) + "\n"

    messagebox.showinfo("Summary", message)


def compare_periods_clicked():
    period_a = simpledialog.askstring("Compare Periods", "Enter first period (YYYY-MM):")
    if not period_a:
        return
    period_b = simpledialog.askstring("Compare Periods", "Enter second period (YYYY-MM):")
    if not period_b:
        return

    comparison = bill_manager.compare_two_periods(bills, period_a, period_b)
    if len(comparison) == 0:
        messagebox.showinfo("Compare Periods", "No data found for these periods.")
        return

    message = "Comparing " + period_a + " vs " + period_b + "\n\n"
    for item in comparison:
        message = message + "- " + item["category"] + ": "
        message = message + str(round(item["period_a_total"], 2)) + " -> "
        message = message + str(round(item["period_b_total"], 2))
        message = message + " (change: " + str(round(item["change"], 2)) + ")\n"

    messagebox.showinfo("Compare Periods", message)


def show_unusual_increases():
    flagged_list = bill_manager.find_unusual_increases(bills)
    if len(flagged_list) == 0:
        messagebox.showinfo("Unusual Increases", "No unusual increases found.")
        return

    message = "Unusual increases found:\n\n"
    for item in flagged_list:
        message = message + "- " + item["category"] + " (" + item["billing_period"] + "): "
        message = message + str(round(item["amount"], 2)) + " - " + item["reason"] + "\n"

    messagebox.showinfo("Unusual Increases", message)


# -----------------------------------------------------
# Chart buttons
# -----------------------------------------------------
def show_bar_chart():
    charts.show_category_bar_chart(bills)


def show_trend_chart():
    charts.show_monthly_trend_chart(bills)


def show_pie_chart():
    charts.show_paid_unpaid_pie_chart(bills)


# -----------------------------------------------------
# Program start
# -----------------------------------------------------
def main():
    global window, bills

    window = tk.Tk()
    window.title("Household Bills Manager")
    window.geometry("950x600")

    try:
        bills = file_handler.load_bills()
    except IOError as error:
        messagebox.showerror("File Error", str(error))
        bills = []

    create_form_section()
    create_search_section()
    create_table_section()
    create_bottom_buttons()
    refresh_table()

    window.mainloop()


if __name__ == "__main__":
    main()
