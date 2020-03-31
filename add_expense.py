#!/usr/bin/env python3
import pandas as pd
import csv
import json
from datetime import date, timedelta, datetime
from argparse import ArgumentParser
from helper_functions import (
    get_max_id,
    print_top_id,
    find_similar_expense_entries,
    check_csv_exists_and_create,
)

# Loads .json file settings
with open("config.json", "r") as f:
    config = json.load(f)

# Sets up expenses df
expense_file_loc = config["expenses_file_location"]
col_names = ["id", "date", "store", "category", "item", "cost"]
dtypes = {
    "id": "int64",
    "date": "str",
    "store": "str",
    "category": "str",
    "item": "str",
    "cost": "float64",
}

check_csv_exists_and_create(expense_file_loc, col_names)

expense_df = pd.read_csv(
    expense_file_loc, dtype=dtypes, names=col_names, header=None, skiprows=1
)

if __name__ == "__main__":

    # id, date, store, category, item, cost
    PARSER = ArgumentParser(
        description="Adds an expense to expense.csv. Must be of the correct format"
    )

    # date
    PARSER.add_argument(
        "-d",
        "--date",
        default=date.today() - timedelta(days=1),
        type=lambda d: datetime.strptime(d, "%Y%m%d").date(),
        help="Date of purchase in the format yyyymmdd",
        required=True,
    )

    # store of purchase
    PARSER.add_argument(
        "-s", "--store", type=str, help="store of purchase", required=True
    )

    # category type of purchase
    PARSER.add_argument(
        "-t", "--type", type=str, help="category type of purchase", required=True
    )

    # store of purchase
    PARSER.add_argument("-i", "--item", type=str, help="purchased item", required=True)

    # cost
    PARSER.add_argument(
        "-c", "--cost", type=float, help="total cost of purchase", required=True
    )

    args = PARSER.parse_args()

    input_date = args.date
    input_store = args.store.lower()
    input_type = args.type.lower()
    input_item = args.item.lower()
    input_cost = args.cost
    input_cost_str = "%.2f" % args.cost

    similar_entries = find_similar_expense_entries(
        expense_df, input_store, float(input_cost_str)
    )

    if not similar_entries.empty:
        print("These similar entries already exist:")
        print(similar_entries)

    # Allow the user to verify that the inputted data is correct
    print(
        "Date: ",
        input_date,
        "\tStore: ",
        input_store,
        "\tCategory: ",
        input_type,
        "\tItem: ",
        input_item,
        "\tCost: ",
        input_cost_str,
    )

    print("\nAdd to expense book? (y/n)")

    choice = input().lower()
    if choice in config["yes"]:

        next_id = get_max_id(expense_df) + 1
        input_date_str = input_date.strftime("%Y-%m-%d")

        next_csv_row = (
            str(next_id)
            + ", "
            + input_date_str
            + ", "
            + input_store
            + ", "
            + input_type
            + ", "
            + input_item
            + ", "
            + input_cost_str
            + "\n"
        )

        # 'a' appends the newline to the end of the file
        with open(expense_file_loc, "a") as csv_file:
            csv_file.write(next_csv_row)

        print("\nRow added to " + expense_file_loc)

        # Append a row to expense_df to avoid re-reading it
        row = [next_id, input_date_str, input_store, input_type, input_item, input_cost]
        expense_df = expense_df.append(pd.DataFrame([row], columns=expense_df.columns))
        print_top_id(expense_df, 5)

    else:
        print("Entry was not added.")
