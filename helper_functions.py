import math
import pandas


def get_max_id(df):
    max_id = df["id"].max()
    return 0 if math.isnan(max_id) else max_id


def print_top_id(df, num_rows):
    # Read in and print the last num_rows of the file.
    if len(df.index) < 5:
        print(df)
    else:
        print(df[df.id > get_max_id(df) - num_rows])
