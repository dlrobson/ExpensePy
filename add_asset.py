#!/usr/bin/env python3
import pandas as pd
import csv
import math

from datetime import date, timedelta, datetime
from argparse import ArgumentParser

yes = {"yes", "y", "ye", "ys", "", " y"}

assets_file_loc = "assets.csv"

colnames = ["id", "date", "source", "description", "amount"]
dtypes = {
    "id": "int64",
    "date": "str",
    "source": "str",
    "description": "str",
    "amount": "float64",
}


def get_max_id():
    expense_df = pd.read_csv(
        assets_file_loc, dtype=dtypes, names=colnames, header=None, skiprows=1
    )
    max_id = expense_df["id"].max()
    return 0 if math.isnan(max_id) else max_id


def print_top_id(num_rows):
    expense_df = pd.read_csv(
        assets_file_loc, dtype=dtypes, names=colnames, header=None, skiprows=1
    )

    # Read in and print the last num_rows of the file.
    if len(expense_df.index < 5):
        print(expense_df)
    else:
        print(expense_df[expense_df.id > get_max_id() - num_rows])


def find_similar_entries(date, source, amount):
    expense_df = pd.read_csv(
        assets_file_loc, dtype=dtypes, names=colnames, header=None, skiprows=1
    )

    expense_df["date"] = pd.to_datetime(
        expense_df["date"].str.strip(), format="%Y-%m-%d"
    )

    date_before = datetime.combine(date - timedelta(days=14), datetime.min.time())
    date_after = datetime.combine(date + timedelta(days=14), datetime.min.time())

    similar_entries = expense_df.loc[
        ((expense_df["date"] < date_after) & (expense_df["date"] > date_before))
        & (expense_df["source"].str.strip() == source)
        & (expense_df["amount"] - amount < 0.01)
    ]

    # print(expense_df.loc[expense_df.store == "Walmart"])
    return similar_entries


if __name__ == "__main__":

    # id, date, store, category, item, cost
    PARSER = ArgumentParser(
        description="Adds an expense to assets.csv. Must be of the correct format"
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

    # source of asset
    PARSER.add_argument(
        "-s", "--source", type=str, help="source of asset", required=True
    )

    # description of asset
    PARSER.add_argument("-t", "--type", type=str, help="type of asset", required=True)

    # amount of asset
    PARSER.add_argument(
        "-a", "--amount", type=float, help="amount of asset", required=True
    )

    args = PARSER.parse_args()

    input_date = args.date
    input_source = args.source.lower()
    input_type = args.type.lower()
    input_amount = "%.2f" % args.amount

    similar_entries = find_similar_entries(
        input_date, input_source, float(input_amount)
    )

    if not similar_entries.empty:
        print("These similar entries already exist:")
        print(similar_entries)

    # Allow the user to verify that the inputted data is correct
    print(
        "Date: ",
        input_date,
        "\tSource: ",
        input_source,
        "\tType: ",
        input_type,
        "\tAmount: ",
        input_amount,
    )

    print("Add to asset book? (y/n)")

    choice = input().lower()
    if choice in yes:
        print("Row added to " + assets_file_loc)
        next_csv_row = (
            str(get_max_id() + 1)
            + ", "
            + input_date.strftime("%Y-%m-%d")
            + ", "
            + input_source
            + ", "
            + input_type
            + ", "
            + input_amount
            + "\n"
        )

        # 'a' appends the newline to the end of the file
        with open(assets_file_loc, "a") as csv_file:
            csv_file.write(next_csv_row)

        print_top_id(5)

    else:
        print("Entry was not added.")
