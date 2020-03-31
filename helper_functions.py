import math
import pandas as pd
from datetime import date, timedelta, datetime


def get_max_id(df):
    max_id = df["id"].max()
    return 0 if math.isnan(max_id) else max_id


def print_top_id(df, num_rows):
    # Read in and print the last num_rows of the file.
    if len(df.index) < 5:
        print(df)
    else:
        print(df[df.id > get_max_id(df) - num_rows])


def find_similar_expense_entries(expense_df, store, cost):
    similar_entries = expense_df.loc[
        (expense_df["store"].str.strip() == store) & (expense_df["cost"] - cost < 0.01)
    ]

    return similar_entries


def find_similar_asset_entries(assets_df, date, source, amount):

    # Converts the col to datetime to be queried
    assets_df["date"] = pd.to_datetime(assets_df["date"].str.strip(), format="%Y-%m-%d")

    # Similar dates are defined as days 2 weeks before or after the entered date
    date_before = datetime.combine(date - timedelta(days=15), datetime.min.time())
    date_after = datetime.combine(date + timedelta(days=15), datetime.min.time())

    similar_entries = assets_df.loc[
        ((assets_df["date"] < date_after) & (assets_df["date"] > date_before))
        & (assets_df["source"].str.strip() == source)
        & (assets_df["amount"] - amount < 0.01)
    ]
    # Converts the date col to be a string again
    assets_df["date"] = assets_df["date"].dt.strftime("%Y-%m-%d")
    return similar_entries
