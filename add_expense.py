#!/usr/bin/env python3
import pandas as pd
import csv
import math

from datetime import date, timedelta, datetime
from argparse import ArgumentParser

yes = {"yes", "y", "ye", "ys", "", " y"}

expense_file_loc = "expenses.csv"

colnames = ["id", "date", "store", "category", "item", "cost"]
dtypes = {
    "id": "int64",
    "date": "str",
    "store": "str",
    "category": "str",
    "item": "str",
    "cost": "float64",
}


def get_max_id():
    expense_df = pd.read_csv(
        expense_file_loc, dtype=dtypes, names=colnames, header=None, skiprows=1
    )
    max_id = expense_df["id"].max()
    return 0 if math.isnan(max_id) else max_id


def print_top_id(num_rows):
    expense_df = pd.read_csv(
        expense_file_loc, dtype=dtypes, names=colnames, header=None, skiprows=1
    )

    # Read in and print the last num_rows of the file.
    if len(expense_df.index < 5):
        print(expense_df)
    else:
        print(expense_df[expense_df.id > get_max_id() - num_rows])


def find_similar_entries(store, cost):
    expense_df = pd.read_csv(
        expense_file_loc, dtype=dtypes, names=colnames, header=None, skiprows=1
    )
    similar_entries = expense_df.loc[
        (expense_df["store"].str.strip() == store) & (expense_df["cost"] - cost < 0.01)
    ]

    # print(expense_df.loc[expense_df.store == "Walmart"])
    return similar_entries


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
    input_cost_str = "%.2f" % args.cost

    similar_entries = find_similar_entries(input_store, float(input_cost_str))

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

    print("Add to expense book? (y/n)")

    choice = input().lower()
    if choice in yes:
        print("Row added to " + expense_file_loc)
        next_csv_row = (
            str(get_max_id() + 1)
            + ", "
            + input_date.strftime("%Y-%m-%d")
            + ", "
            + input_store
            + ", "
            + args.type
            + ", "
            + input_item
            + ", "
            + input_cost_str
            + "\n"
        )

        # 'a' appends the newline to the end of the file
        with open(expense_file_loc, "a") as csv_file:
            csv_file.write(next_csv_row)

        print_top_id(5)

    else:
        print("Entry was not added.")
