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

# Function to format dates
def format_date(date_str):
    try:
        return pd.to_datetime(date_str).strftime('%m/%d/%y')
    except ValueError:
        return date_str

def process_futures_data(file_path):
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
            # filtered_contract['ObservationData'] = observations_with_uniform_k # includes only obs=k
            filtered_contract['ObservationData'] = contract['ObservationData'] #includes all
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

def find_highest_calendar_k(contracts_list):
    # Initialize the highest CalendarK value to a very small number
    highest_calendar_k = -1

    # Iterate through each contract in the list
    for contract in contracts_list:
        # Iterate through each observation in the contract
        for observation in contract['ObservationData']:
            # Update the highest CalendarK if the current one is higher
            if observation['CalendarK'] > highest_calendar_k:
                highest_calendar_k = observation['CalendarK']

    return highest_calendar_k

# Example usage:
# highest_k = find_highest_calendar_k(contracts_list)
# print("The highest CalendarK in the contracts list is:", highest_k)

def read_spot_prices_from_csv(input_path):
    # Read the CSV file
    data = pd.read_csv(input_path)
    
    # Assuming the first column contains dates and the second column contains spot prices
    date_column = data.columns[0]
    spot_price_column = data.columns[1]
    
    # Format the dates in the DataFrame
    data[date_column] = data[date_column].apply(format_date)
    
    # Convert the DataFrame to a dictionary with formatted date strings as keys and spot prices as values
    spot_prices_dict = pd.Series(data[spot_price_column].values, index=data[date_column]).to_dict()
    
    return spot_prices_dict

# Example usage:
# spot_prices = read_spot_prices_from_csv('path_to_your_csv_file.csv')
# print(spot_prices)


def get_observation_at_k(contract,k):
    for observation in contract['ObservationData']:
        if int(observation['CalendarK']) == k:
            return observation


# Creating JSON from CSV:
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

# Filtering for only contracts with expiration date observations:
# list_load_path = get_contracts_in_path()
# loaded_contracts_list = load_contracts_from_json(list_load_path)
# # print(str(loaded_contracts_list[0])) #it works!

# # highest_k = find_highest_calendar_k(loaded_contracts_list)
# # print("The highest CalendarK in the contracts list is:", highest_k) #125

# contracts_with_expiration_observations = filter_contracts_by_uniform_k(loaded_contracts_list, 0)
# highest_k = find_highest_calendar_k(contracts_with_expiration_observations)
# print("The highest CalendarK in the contracts list is:", highest_k) # 125 still
# list_save_path = get_contracts_out_path() # contracts_with_expiration_observations.json
# save_contracts_to_json(contracts_with_expiration_observations,list_save_path)

# Next step: ensure we even still have enough contracts to do what we need to here.
# list_load_path = get_contracts_in_path()
# loaded_contracts_list = load_contracts_from_json(list_load_path)
# print(str(len(loaded_contracts_list)))
# # saved_contracts_list.json = 141
# # contracts_with_expiration_observations.json = 140
# # good enough for government work!

# Next step: create list of contracts lists filtered for every value of K 
# list_load_path = get_contracts_in_path()
# loaded_contracts_list = load_contracts_from_json(list_load_path)
# highest_k = int(find_highest_calendar_k(loaded_contracts_list))
# list_of_uniform_k_lists = []
# list_of_lengths = []
# for k in range(highest_k):
#     list_of_uniform_k_lists.append(filter_contracts_by_uniform_k(loaded_contracts_list, k))
#     list_of_lengths.append(len(list_of_uniform_k_lists[k]))
# list_save_path = get_contracts_out_path()
# save_contracts_to_json(list_of_uniform_k_lists,list_save_path) # list_of_uniform_k_lists.json
# print(list_of_lengths)

# Next step: load in spot data as dictionary
# spot_prices_csv_path = get_data_path()
# spot_prices_dict = read_spot_prices_from_csv(spot_prices_csv_path)
# # print(spot_prices_dict) #it works!
# spot_save_path = get_contracts_out_path()
# save_contracts_to_json(spot_prices_dict, spot_save_path) # spot_dict.json

# Next step:
spot_load_path = get_contracts_in_path()
spot_prices_dict = load_contracts_from_json(spot_load_path)

list_load_path = get_contracts_in_path()
list_of_uniform_k_lists = load_contracts_from_json(list_load_path)

k = 63
test_contract_list = list_of_uniform_k_lists[k]
s_t_values = []
s_t_minus_k_values = []
f_t_t_minus_k_values = []
for contract in test_contract_list:

    observation_at_expiry = get_observation_at_k(contract,0)
    observation_at_k = get_observation_at_k(contract,k)

    expiry_date = observation_at_expiry['ObservationDate']
    k_date = observation_at_k['ObservationDate']



    s_t_values.append(spot_prices_dict[expiry_date])
    s_t_minus_k_values.append(spot_prices_dict[k_date])
    f_t_t_minus_k_values.append(observation_at_k['ContractPrice'])

print("\ns_t_values:")
print(s_t_values)
print("\ns_t_minus_k_values:")
print(s_t_minus_k_values)
print("\nf_t_t_minus_k_values:")
print(f_t_t_minus_k_values)

# test_contracts_save_path = get_contracts_out_path()
# save_contracts_to_json(test_contract_list, test_contracts_save_path) # test_contract_list.json

print("done")