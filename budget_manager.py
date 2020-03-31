#!/usr/bin/env python3
import json
from argparse import ArgumentParser
from datetime import date, timedelta, datetime

# Loads .json file settings
with open("config.json", "r") as f:
    config = json.load(f)

# Sets up expenses df
budget_file_loc = config["budget_file_location"]


def sort_budget_json_file():
    print(budget_file_loc)
    pass


# if month doesn't exist, add month entry
# if year doesn't exist, add year entry
# Add budget type
def add_category(added_category, date):
    pass


def edit_category_budget(category, date):
    pass


# Delete category
def remove_category(removed_category, date):
    pass


def view_month_budget(month):
    pass


def view_budget_histories():
    pass


if __name__ == "__main__":

    PARSER = ArgumentParser(
        description="Adds an expense to income.csv. Must be of the correct format",
    )

    # To add a category type
    PARSER.add_argument(
        "-a", "--add", type=str, help="category to add to the current budget rules",
    )

    # To add a category type
    PARSER.add_argument(
        "-b",
        "--budget",
        type=float,
        help="category to add to the current budget rules",
    )

    # To remove a category type
    PARSER.add_argument(
        "-r",
        "--remove",
        type=str,
        help="category to remove from the current budget rules",
    )

    # date to apply adjusted budget settings
    PARSER.add_argument(
        "-d",
        "--date",
        default=date.today().replace(day=1),
        type=lambda d: datetime.strptime(d, "%Y%m").date(),
        help="Date of purchase in the format yyyymm. If no date is provided, then the default is today's month.",
    )

    args = PARSER.parse_args()

    if args.add and not args.budget:
        PARSER.error("--add requires --budget")

    if args.add:
        add_category(args.add, args.date)
    elif args.remove:
        remove_category(args.remove, args.date)
