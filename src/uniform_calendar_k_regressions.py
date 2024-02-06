import statsmodels.api as sm
import json
from datetime import datetime
import tkinter as tk
from tkinter import filedialog
from tkinter.filedialog import askdirectory
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from statsmodels.stats.diagnostic import het_white

def get_data():
    filetypes = (("CSV files", "*.csv"), ("All files", "*.*"))
    path = filedialog.askopenfilename(filetypes=filetypes)
    print("Chose file at " + path)
    data = pd.read_csv(path)
    return data

def get_output_results_path_txt():
    filetypes = (("Text files", "*.txt"), ("All files", "*.*"))
    path = filedialog.asksaveasfilename(filetypes=filetypes)
    return path

def get_output_results_path_json():
    filetypes = (("JSON files", "*.json"), ("All files", "*.*"))
    path = filedialog.asksaveasfilename(filetypes=filetypes)
    return path

def get_dir():
    dir = askdirectory(title='Select Folder')
    return dir

def k_to_max_lags(k):
    # return 2*(k-1)
    return max(1, round(((k-30) / 30)*2))

def run_regression_and_wald_test(data, k, output_file_path):
    X = data[['ln(Ft,t-k) - ln(St-k)']]  # Independent variable
    y = data['ln(St) - ln(St-k)']  # Dependent variable
    X = sm.add_constant(X)  # Add a constant term for the intercept
    
    max_lags = k_to_max_lags(k)

    # Fit the OLS model with HAC (Newey-West) standard errors
    model = sm.OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags': max_lags})
    
    # Define the joint hypothesis for Wald test: a=0 and b=1
    hypothesis = '(const = 0), (ln(Ft,t-k) - ln(St-k) = 1)'
    
    # Perform the Wald test
    wald_test_result = model.wald_test(hypothesis)
    
    # Save results
    with open(output_file_path, 'w') as file:
        file.write("Results for Uniform Calendar k = " + str(k)+":\n")
        file.write(("_"*89)+"\n")
        file.write(model.summary().as_text())
        file.write("\n\nWald Test Result (p-value for joint hypothesis a=0 and b=1):\n")
        file.write(str(wald_test_result.pvalue))
    
    print("Analysis complete. Results saved to:", output_file_path)

# Example usage
# run_regression_and_wald_test(data, k, "output.txt")

def run_regression_and_wald_test_json(data, k, output_json_path):
    X = sm.add_constant(data[['ln(Ft,t-k) - ln(St-k)']])  # Independent variable with constant
    y = data['ln(St) - ln(St-k)']  # Dependent variable
    model = sm.OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags': 2*(k-1)})

    # Perform the Wald test with the specified hypothesis
    hypothesis = '(const = 0), (ln(Ft,t-k) - ln(St-k) = 1)'
    wald_test_result = model.wald_test(hypothesis)

    # Convert model attributes to serializable formats
    ci = model.conf_int().applymap(float)  # Convert confidence intervals to float

    result_data = {
        "Uniform Calendar k": k,
        # Include model summary attributes
        "Dep. Variable": model.model.endog_names,
        # Other attributes...
        "Parameter Results": [
            {
                "Parameter Name": name,
                "coef": float(model.params[name]),
                "std err": float(model.bse[name]),
                "z": float(model.tvalues[name]),
                "P>|z|": float(model.pvalues[name]),
                "95% CI": {
                    "Lower": ci.loc[name, 0],
                    "Upper": ci.loc[name, 1]
                }
            } for name in model.params.index
        ],
        "Wald Test Result": float(wald_test_result.pvalue)  # Ensure p-value is float
    }

    # Serialize to JSON, ensuring all values are serializable
    with open(output_json_path, 'w') as json_file:
        json.dump(result_data, json_file, indent=4)

    print("Analysis complete. Results saved to:", output_json_path)

# Example usage
# run_regression_and_wald_test_json(data, k, "output.json")

def run_all_regressions(input_dir_path, output_dir_path):
    for k in range(125)[1:]:
        print("\n"+("_"*89)+"\nRunning regression for Uniform Calendar k = "+str(k)+":\n")
        input_file_name = "uniform_calendar_k_" + str(k) + ".csv"
        input_path = os.path.join(input_dir_path, input_file_name)
        data = pd.read_csv(input_path)
        output_txt_file_name = "uniform_calendar_k_" + str(k) + ".txt"
        output_json_file_name = "uniform_calendar_k_" + str(k) + ".json"
        output_results_path_txt = os.path.join(output_dir_path, output_txt_file_name)
        output_results_path_json = os.path.join(output_dir_path, output_json_file_name)
        run_regression_and_wald_test(data, k, output_results_path_txt)
        run_regression_and_wald_test_json(data, k, output_results_path_json)

# Next step:
# k = 63
# data = get_data()
# # output_results_path_txt = get_output_results_path_txt()
# output_results_path_json = get_output_results_path_json()
# # run_regression_and_wald_test(data, k, output_results_path_txt)
# run_regression_and_wald_test_json(data, k, output_results_path_json)

# Next step:
# k = 63
# input_dir_path = get_dir()
# input_file_name = "uniform_calendar_k_" + str(k) + ".csv"
# input_path = os.path.join(input_dir_path, input_file_name)
# data = pd.read_csv(input_path)

# output_dir_path = get_dir()
# output_txt_file_name = "uniform_calendar_k_" + str(k) + ".txt"
# output_json_file_name = "uniform_calendar_k_" + str(k) + ".json"
# output_results_path_txt = os.path.join(output_dir_path, output_txt_file_name)
# output_results_path_json = os.path.join(output_dir_path, output_json_file_name)

# run_regression_and_wald_test(data, k, output_results_path_txt)
# run_regression_and_wald_test_json(data, k, output_results_path_json)

# Next step:
input_dir_path = get_dir()
output_dir_path = get_dir()
run_all_regressions(input_dir_path, output_dir_path)

print("All done!")