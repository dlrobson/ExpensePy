#!/usr/bin/env python3
import math
import os
import json
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


def find_similar_income_entries(income_df, date_in, source, amount):

    # Converts the col to datetime to be queried
    income_df["date"] = pd.to_datetime(income_df["date"].str.strip(), format="%Y-%m-%d")

    # Similar dates are defined as days 2 weeks before or after the entered date
    date_before = datetime.combine(date_in - timedelta(days=15), datetime.min.time())
    date_after = datetime.combine(date_in + timedelta(days=15), datetime.min.time())

    similar_entries = income_df.loc[
        ((income_df["date"] < date_after) & (income_df["date"] > date_before))
        & (income_df["source"].str.strip() == source)
        & (income_df["amount"] - amount < 0.01)
    ]
    # Converts the date col to be a string again
    income_df["date"] = income_df["date"].dt.strftime("%Y-%m-%d")
    return similar_entries


def find_budget_month(budget_file_loc, input_date):

    # Check if file exists. If not, return
    if not os.path.exists(budget_file_loc):
        return

    # Loads budget json file
    with open(budget_file_loc, "r") as f:
        budget = json.load(f)

        # Finds the monthly budget that applies to the budget date
        # Convert the keys to integers, and hold the years of the budget.
        years = {int(year_key): val for year_key, val in budget.items()}
        budget_dates = []
        for year in years:
            months = {
                int(month_key): val for month_key, val in budget[str(year)].items()
            }
            for month in months:
                budget_date = date(year, month, 1)
                budget_dates.append(budget_date)

        # budget_dates holds all of the dates that contain a budget. Sort the list, so
        # that the first date found is the correct budget date to use.
        budget_dates.sort(reverse=True)
        for budget_date in budget_dates:
            if budget_date <= input_date:
                return budget_date
        # return the first budget if no budget was found.
        if len(budget_dates) != 0:
            return budget_dates[-1]
        else:
            return None


# https://www.datacamp.com/community/tutorials/fuzzy-string-python
# https://towardsdatascience.com/fuzzy-string-matching-in-python-68f240d910fe
def fuzzy_match(input_str, list):
    pass
