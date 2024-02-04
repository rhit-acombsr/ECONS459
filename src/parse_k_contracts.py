import pandas as pd
from tkinter import filedialog
import tkinter as tk
import json

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

def filter_contracts_by_uniform_k(contracts_list, uniform_k):
    # Create a new list to store the filtered contracts
    filtered_contracts = []

    # Iterate through each contract
    for contract in contracts_list:
        # Check if there is any observation data with the specified uniform_k value
        observations_with_uniform_k = [obs for obs in contract['ObservationData'] if obs['CalendarK'] == uniform_k]

        # Include the contract only if it has observation data with uniform_k
        if observations_with_uniform_k:
            # Creating a copy of the contract with filtered observations
            filtered_contract = contract.copy()
            filtered_contract['ObservationData'] = observations_with_uniform_k
            filtered_contracts.append(filtered_contract)

    return filtered_contracts

# Example usage:
# filtered_list = filter_contracts_by_uniform_k(contracts_list, uniform_k_value)

def add_expiration_dates_to_contracts(contracts_list, expiration_dates_csv_path):
    # Read the CSV file containing expiration dates
    expiration_dates_df = pd.read_csv(expiration_dates_csv_path)

    # Create a mapping of contract names to expiration dates
    expiration_dates_map = dict(zip(expiration_dates_df['ContractName'], expiration_dates_df['ExpirationDate']))

    # Update each contract in the contracts_list with its expiration date
    for contract in contracts_list:
        contract_name = contract['ContractName']
        expiration_date = expiration_dates_map.get(contract_name, None)
        if expiration_date:
            contract['ExpirationDate'] = expiration_date

    return contracts_list

# Example usage:
# updated_contracts_list = add_expiration_dates_to_contracts(contracts_list, 'path_to_expiration_dates_csv.csv')

def get_contracts_in_path():
    filetypes = (("Contract List JSON", "*.json"), ("All files", "*.*"))
    path = filedialog.askopenfilename(filetypes=filetypes)
    return path

def get_contracts_out_path():
    filetypes = (("Contract List JSON", "*.json"), ("All files", "*.*"))
    path = filedialog.asksaveasfilename(filetypes=filetypes)
    return path

def save_contracts_to_json(contracts_list, output_path):
    with open(output_path, 'w') as json_file:
        json.dump(contracts_list, json_file, indent=4)

# Example usage:
# save_contracts_to_json(contracts_list, 'path_to_output.json')

def load_contracts_from_json(input_path):
    with open(input_path, 'r') as json_file:
        contracts_list = json.load(json_file)
    return contracts_list

# Example usage:
# contracts_list = load_contracts_from_json('path_to_input.json')

# # Example usage:
# csv_path = get_data_path()
# contracts_list = process_futures_data(csv_path)
# # print(str(type(contracts_list))) #list
# # print(str(type(contracts_list[0]))) #dict
# # print(str(contracts_list[0])) #it works!
# # print(str(updated_contracts_list[0])) #it works!
# csv_path = get_data_path()
# updated_contracts_list = add_expiration_dates_to_contracts(contracts_list, csv_path)

# list_save_path = get_contracts_out_path() #saved_contracts_list.json
# save_contracts_to_json(updated_contracts_list,list_save_path)

list_load_path = get_contracts_in_path()
loaded_contracts_list = load_contracts_from_json(list_load_path)
print(str(loaded_contracts_list[0])) #it works!


print("done")