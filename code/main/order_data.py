import pandas as pd


def select_data(data, item=None, day=None):
    new_data = data.copy()
    if item:
        new_data = new_data.loc[data['items'].str.contains(item, case=False)]
    if day:
        new_data = new_data.loc[data['days'].str.contains(day, case=False)]
    return new_data
