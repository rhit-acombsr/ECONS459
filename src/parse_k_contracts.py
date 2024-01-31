import pandas as pd
from tkinter import filedialog
import tkinter as tk

def get_data_path():
    filetypes = (("CSV files", "*.csv"), ("All files", "*.*"))
    path = filedialog.askopenfilename(filetypes=filetypes)
    # print("Chose file at " + path)
    # data = pd.read_csv(path)
    # return data
    return path

def process_futures_data(file_path):
    # Function to format dates
    def format_date(date_str):
        try:
            return pd.to_datetime(date_str).strftime('%m/%d/%y')
        except ValueError:
            return date_str

    # Read the CSV file
    data = pd.read_csv(file_path)

    # Dictionary to hold contract data
    contracts = {}

    # Iterate over the columns, skipping the first one (observation dates)
    for i in range(1, len(data.columns), 2):
        contract_name = data.columns[i].split('_')[0]
        if contract_name not in contracts:
            contracts[contract_name] = {
                'ContractName': contract_name,
                'ObservationData': []
            }

        # Iterate over rows to get observation data
        for index, row in data.iterrows():
            price = row[i]
            k_value = row[i + 1]

            # Skip if either price or K value is missing
            if pd.isna(price) or pd.isna(k_value):
                continue

            observation_data = {
                'ObservationDate': format_date(row[0]),
                'ContractPrice': price,
                'CalendarK': k_value
            }
            contracts[contract_name]['ObservationData'].append(observation_data)

    # Convert to list of contract objects
    return list(contracts.values())

# Example usage:
csv_path = get_data_path()
contracts_list = process_futures_data(csv_path)
# print(str(type(contracts_list))) #list
# print(str(type(contracts_list[0]))) #dict
# print(str(contracts_list[0])) #it works!
print("done")