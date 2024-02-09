import os
import re
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askdirectory

def get_dir():
    dir = askdirectory(title='Select Folder')
    return dir

def get_output_path_csv():
    filetypes = (("CSV files", "*.csv"), ("All files", "*.*"))
    path = filedialog.asksaveasfilename(filetypes=filetypes)
    return path

def extract_values_from_txt(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        
        # Extract k, R-squared, and No. Observations using regular expressions
        k_match = re.search(r'Results for Uniform Calendar k = (\d+):', content)
        r_squared_match = re.search(r'R-squared:\s+([\d.]+)', content)
        observations_match = re.search(r'No. Observations:\s+(\d+)', content)
        
        # Convert matches to appropriate types
        k = int(k_match.group(1)) if k_match else None
        r_squared = float(r_squared_match.group(1)) if r_squared_match else None
        observations = int(observations_match.group(1)) if observations_match else None
        
        return k, r_squared, observations

def tabulate_results(input_dir_path, output_csv_path):
    results = []
    
    # Iterate over all files in the input directory
    for filename in os.listdir(input_dir_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(input_dir_path, filename)
            k, r_squared, observations = extract_values_from_txt(file_path)
            results.append((k, r_squared, observations))
    
    # Convert results to a DataFrame and save as CSV
    df = pd.DataFrame(results, columns=['Uniform Calendar k', 'R-squared', 'No. Observations'])
    df.to_csv(output_csv_path, index=False)

# Example usage
# input_dir_path = 'path/to/your/input/directory'
# output_csv_path = 'path/to/your/output/results.csv'
# tabulate_results(input_dir_path, output_csv_path)

input_dir_path = get_dir()
output_csv_path = get_output_path_csv()
tabulate_results(input_dir_path, output_csv_path)

print("All done!")