#!/usr/bin/env python3
import pandas as pd
import os
import csv
import json
from datetime import date, timedelta, datetime
from argparse import ArgumentParser
from helper_functions import (
    get_max_id,
    print_top_id,
    find_similar_income_entries,
    check_csv_exists_and_create,
)

# Loads .json file settings
with open("config.json", "r") as f:
    config = json.load(f)

# Sets up income df
income_file_loc = config["income_file_location"]
print(income_file_loc)
col_names = ["id", "date", "source", "description", "amount"]
dtypes = {
    "id": "int64",
    "date": "str",
    "source": "str",
    "description": "str",
    "amount": "float64",
}

check_csv_exists_and_create(income_file_loc, col_names)

income_df = pd.read_csv(
    income_file_loc, dtype=dtypes, names=col_names, header=None, skiprows=1
)


if __name__ == "__main__":

    # id, date, store, category, item, cost
    PARSER = ArgumentParser(
        description="Adds an income to income.csv. Must be of the correct format"
    )

    # date
    PARSER.add_argument(
        "-d",
        "--date",
        default=date.today(),
        type=lambda d: datetime.strptime(d, "%Y%m%d").date(),
        help="Date of purchase in the format yyyymmdd",
        required=True,
    )

    # source of income
    PARSER.add_argument(
        "-s", "--source", type=str, help="source of income", required=True
    )

    # description of income
    PARSER.add_argument("-t", "--type", type=str, help="type of income", required=True)

    # amount of income
    PARSER.add_argument(
        "-a", "--amount", type=float, help="amount of income", required=True
    )

    args = PARSER.parse_args()

    input_date = args.date
    input_source = args.source.lower()
    input_type = args.type.lower()
    input_amount = "%.2f" % args.amount

    similar_entries = find_similar_income_entries(
        income_df, input_date, input_source, float(input_amount)
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

    print("\nAdd to income book? (y/n)")

    choice = input().lower()
    if choice in config["yes"]:

        next_id = get_max_id(income_df) + 1
        input_date_str = input_date.strftime("%Y-%m-%d")

        next_csv_row = (
            str(next_id)
            + ", "
            + input_date_str
            + ", "
            + input_source
            + ", "
            + input_type
            + ", "
            + input_amount
            + "\n"
        )

        # 'a' appends the newline to the end of the file
        with open(income_file_loc, "a") as csv_file:
            csv_file.write(next_csv_row)

        print("\nRow added to " + income_file_loc)

        # Append a row to income_df to avoid re-reading it
        row = [next_id, input_date, input_source, input_type, input_amount]
        income_df = income_df.append(pd.DataFrame([row], columns=income_df.columns))
        print_top_id(income_df, 5)

    else:
        print("Entry was not added.")
