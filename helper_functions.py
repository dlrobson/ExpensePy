import math
import os
import pandas as pd
from datetime import date, timedelta, datetime


def check_csv_exists_and_create(file_loc, col_names):
    # Check if file exists. If not, create it
    if not os.path.exists(file_loc):
        # w+ open the file for updating, and truncates
        f = open(file_loc, "w+")
        for key in col_names:
            f.write(key)
            if key is not col_names[-1]:
                f.write(",")
        f.write("\n")
        f.close()


def get_max_id(df):
    max_id = df["id"].max()
    return -1 if math.isnan(max_id) else max_id


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


def find_similar_income_entries(income_df, date, source, amount):

    # Converts the col to datetime to be queried
    income_df["date"] = pd.to_datetime(income_df["date"].str.strip(), format="%Y-%m-%d")

    # Similar dates are defined as days 2 weeks before or after the entered date
    date_before = datetime.combine(date - timedelta(days=15), datetime.min.time())
    date_after = datetime.combine(date + timedelta(days=15), datetime.min.time())

    similar_entries = income_df.loc[
        ((income_df["date"] < date_after) & (income_df["date"] > date_before))
        & (income_df["source"].str.strip() == source)
        & (income_df["amount"] - amount < 0.01)
    ]
    # Converts the date col to be a string again
    income_df["date"] = income_df["date"].dt.strftime("%Y-%m-%d")
    return similar_entries


# https://www.datacamp.com/community/tutorials/fuzzy-string-python
# https://towardsdatascience.com/fuzzy-string-matching-in-python-68f240d910fe
def fuzzy_match(input_str, list):
    pass
