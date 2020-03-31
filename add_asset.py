#!/usr/bin/env python3
import pandas as pd
import csv
import json
from datetime import date, timedelta, datetime
from argparse import ArgumentParser
from helper_functions import get_max_id, print_top_id

with open("config.json", "r") as f:
    config = json.load(f)

assets_file_loc = config["assets_file_location"]
yes = config["yes"]

# assets_file_loc = "assets.csv"

colnames = ["id", "date", "source", "description", "amount"]
dtypes = {
    "id": "int64",
    "date": "str",
    "source": "str",
    "description": "str",
    "amount": "float64",
}


def find_similar_entries(date, source, amount):
    assets_df = pd.read_csv(
        assets_file_loc, dtype=dtypes, names=colnames, header=None, skiprows=1
    )

    assets_df["date"] = pd.to_datetime(assets_df["date"].str.strip(), format="%Y-%m-%d")

    date_before = datetime.combine(date - timedelta(days=15), datetime.min.time())
    date_after = datetime.combine(date + timedelta(days=15), datetime.min.time())

    similar_entries = assets_df.loc[
        ((assets_df["date"] < date_after) & (assets_df["date"] > date_before))
        & (assets_df["source"].str.strip() == source)
        & (assets_df["amount"] - amount < 0.01)
    ]

    # print(assets_df.loc[assets_df.store == "Walmart"])
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

    print("\nAdd to asset book? (y/n)")

    choice = input().lower()
    if choice in yes:

        assets_df = pd.read_csv(
            assets_file_loc, dtype=dtypes, names=colnames, header=None, skiprows=1
        )

        next_id = get_max_id(assets_df) + 1
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
        with open(assets_file_loc, "a") as csv_file:
            csv_file.write(next_csv_row)

        print("\nRow added to " + assets_file_loc)

        # Append a row to assets_df to avoid re-reading it
        row = [next_id, input_date_str, input_source, input_type, input_amount]
        assets_df = assets_df.append(pd.DataFrame([row], columns=assets_df.columns))
        print_top_id(assets_df, 5)

    else:
        print("Entry was not added.")
