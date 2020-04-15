#!/usr/bin/env python3
import json
import os
from argparse import ArgumentParser
from datetime import date, timedelta, datetime
from helper_functions import find_budget_month

# Loads config.json file settings
with open("config.json", "r") as f:
    config = json.load(f)

budget_file_loc = config["budget_file_location"]

# Check if file exists. If not, create it
if not os.path.exists(budget_file_loc):
    # w+ open the file for updating, and truncates
    f = open(budget_file_loc, "w+")
    f.write("{}")
    f.close()

# Loads budget json file
with open(budget_file_loc, "r") as f:
    budget = json.load(f)


# Add budget type
def add_category(new_category, budget_val, input_date):

    new_category = new_category.lower()

    try:
        if (
            new_category
            in budget[str(input_date.year)][str(input_date.month)]["categories"]
        ):
            print(
                "Input category already exists. The category value will be updated with the new budget."
            )

        # Month exists, but category does not
        budget[str(input_date.year)][str(input_date.month)]["categories"][
            new_category
        ] = budget_val

    # Month or year does not exist
    except:

        budget_date_to_copy = find_budget_month(budget_file_loc, input_date)

        month_data = {}

        if budget_date_to_copy == None:

            # Sets the category val to hold what was inputeted
            new_key = {}
            new_key[new_category] = budget_val

            month_data["categories"] = new_key

        else:

            month_data["categories"] = budget[str(budget_date_to_copy.year)][
                str(budget_date_to_copy.month)
            ]["categories"]

        # Year does not exist
        if str(input_date.year) not in budget:

            # Add the year to the json file
            year_data = {}
            year_data[str(input_date.month)] = month_data

            budget[str(input_date.year)] = year_data

        # Year exists, but not the month
        else:

            # Add the month to the json year
            budget[str(input_date.year)][str(input_date.month)] = month_data

    with open(budget_file_loc, "w") as f:
        f.write(json.dumps(budget, sort_keys=True, indent=4, separators=(",", ": ")))

    # Print out new budget for that month
    print(
        input_date,
        ":",
        json.dumps(
            budget[str(input_date.year)][str(input_date.month)]["categories"],
            indent=4,
            sort_keys=True,
        ),
    )


# Delete category
def remove_category(removed_category, date):

    removed_category = removed_category.lower()

    try:
        # Remove the category from the dictionary
        budget[str(date.year)][str(date.month)]["categories"].pop(removed_category)

        # Print the updated category list for the user
        print(
            date,
            ":",
            json.dumps(
                budget[str(date.year)][str(date.month)], indent=4, sort_keys=True,
            ),
        )

        # if the month is now empty of categories, remove the month
        if not budget[str(date.year)][str(date.month)]["categories"]:
            budget[str(date.year)].pop(str(date.month))

            # Remove the year if it's empty
            if not budget[str(date.year)]:
                budget.pop(str(date.year))

        with open(budget_file_loc, "w") as f:
            f.write(
                json.dumps(budget, sort_keys=True, indent=4, separators=(",", ": "))
            )

    except:
        print("Category does not exist")


def remove_month(date):

    try:
        budget[str(date.year)].pop(str(date.month))

        # Remove the year if it's empty
        if not budget[str(date.year)]:
            budget.pop(str(date.year))
        with open(budget_file_loc, "w") as f:
            f.write(
                json.dumps(budget, sort_keys=True, indent=4, separators=(",", ": "))
            )
    except:
        print("Month-year pair budget does not exist in " + budget_file_loc)


def view_month_budget(date):
    try:
        print(
            date,
            ":",
            json.dumps(
                budget[str(date.year)][str(date.month)]["categories"],
                indent=4,
                sort_keys=True,
            ),
        )
    except:
        print("Month-year pair budget does not exist in " + budget_file_loc)


# Questionable
def view_budget_history():
    print(json.dumps(budget, indent=4, sort_keys=True))


def month_budget_report(month):
    pass


def annual_budget_report(year):
    pass


if __name__ == "__main__":

    PARSER = ArgumentParser(description="budget.json manager.",)

    # To add a category type
    PARSER.add_argument(
        "-a",
        "--add",
        type=str,
        help="add/edit current budget rules. Supply a -b and -d.",
    )

    # To add a category type
    PARSER.add_argument(
        "-b", "--budget", type=float, help="adjusted budget value",
    )

    # To add a category type
    PARSER.add_argument(
        "-hist", "--history", dest="history", action="store_true", help="Use",
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
        help="Format yyyymm. Date for input budget. If no date is provided, then the default is today's month.",
    )

    # date to apply adjusted budget settings
    PARSER.add_argument(
        "-rmon",
        "--removemonth",
        type=lambda d: datetime.strptime(d, "%Y%m").date(),
        help="Format yyyymm. Date for input budget.",
    )

    # date to apply adjusted budget settings
    PARSER.add_argument(
        "-c",
        "--copymonth",
        type=lambda d: datetime.strptime(d, "%Y%m").date(),
        help="Format yyyymm. Copies the previous budget to the month entered",
    )

    # date to apply adjusted budget settings
    PARSER.add_argument(
        "-pmon",
        "--printmonth",
        type=lambda d: datetime.strptime(d, "%Y%m").date(),
        help="Format yyyymm. Date for input budget.",
    )

    args = PARSER.parse_args()

    if args.add and not args.budget:
        PARSER.error("--add requires --budget")

    if args.add:
        add_category(args.add, args.budget, args.date)

    if args.copymonth:
        copy_month(args.copymonth)

    elif args.remove:
        remove_category(args.remove, args.date)

    if args.removemonth is not None:
        remove_month(args.removemonth)

    if args.printmonth is not None:
        view_month_budget(args.printmonth)

    if args.history:
        view_budget_history()
