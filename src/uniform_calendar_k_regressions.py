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

def get_output_path_csv():
    filetypes = (("CSV files", "*.csv"), ("All files", "*.*"))
    path = filedialog.asksaveasfilename(filetypes=filetypes)
    return path

def get_output_results_path_txt():
    filetypes = (("Text files", "*.txt"), ("All files", "*.*"))
    path = filedialog.asksaveasfilename(filetypes=filetypes)
    return path

def get_output_results_path_json():
    filetypes = (("JSON files", "*.json"), ("All files", "*.*"))
    path = filedialog.asksaveasfilename(filetypes=filetypes)
    return path

def get_json_in_path():
    filetypes = (("Contract List JSON", "*.json"), ("All files", "*.*"))
    path = filedialog.askopenfilename(filetypes=filetypes)
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

def load_dictionary_from_json(input_path):
    with open(input_path, 'r') as json_file:
        loaded_dictionary = json.load(json_file)
    return loaded_dictionary

def tabulate_results(input_dir_path, output_csv_path):
    Uniform_Calendar_k = []
    coef_a = []
    std_err_a = []
    z_a = []
    P_greater_z_a = []
    CI_Lower_a = []
    CI_Upper_a = []
    coef_b = []
    std_err_b = []
    z_b = []
    P_greater_z_b = []
    CI_Lower_b = []
    CI_Upper_b = []
    Wald_Test_Result = []

    for k in range(125)[1:]:
        input_json_file_name = "uniform_calendar_k_" + str(k) + ".json"
        input_results_path_json = os.path.join(input_dir_path, input_json_file_name)
        loaded_dictionary = load_dictionary_from_json(input_results_path_json)

        a = loaded_dictionary["Parameter Results"][0]
        b = loaded_dictionary["Parameter Results"][1]

        Uniform_Calendar_k.append(int(loaded_dictionary["Uniform Calendar k"]))
        coef_a.append(float(a["coef"]))
        std_err_a.append(float(a["std err"]))
        z_a.append(float(a["z"]))
        P_greater_z_a.append(float(a["P>|z|"]))
        CI_Lower_a.append(float(a["95% CI"]["Lower"]))
        CI_Upper_a.append(float(a["95% CI"]["Upper"]))
        coef_b.append(float(b["coef"]))
        std_err_b.append(float(b["std err"]))
        z_b.append(float(b["z"]))
        P_greater_z_b.append(float(b["P>|z|"]))
        CI_Lower_b.append(float(b["95% CI"]["Lower"]))
        CI_Upper_b.append(float(b["95% CI"]["Upper"]))
        Wald_Test_Result.append(float(loaded_dictionary["Wald Test Result"]))

    df = pd.DataFrame({
        'Uniform Calendar k':Uniform_Calendar_k,
        'coef(a)':coef_a,
        'std err(a)':std_err_a,
        'z(a)':z_a,
        'P>|z|(a)':P_greater_z_a,
        '95% CI Lower(a)':CI_Lower_a,
        '95% CI Upper(a)':CI_Upper_a,
        'coef(b)':coef_b,
        'std err(b)':std_err_b,
        'z(b)':z_b,
        'P>|z|(b)':P_greater_z_b,
        '95% CI Lower(b)':CI_Lower_b,
        '95% CI Upper(b)':CI_Upper_b,
        'Wald Test Result':Wald_Test_Result
    })

    df.to_csv(output_csv_path, index=False)

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
# input_dir_path = get_dir()
# output_dir_path = get_dir()
# run_all_regressions(input_dir_path, output_dir_path)

# Next step:
# input_path = get_json_in_path()
# loaded_dictionary = load_dictionary_from_json(input_path)
# k = int(loaded_dictionary["Uniform Calendar k"])
# # print(loaded_dictionary)
# # print("k = " + str(k))
# # print(str(type(k)))

# a = loaded_dictionary["Parameter Results"][0]
# b = loaded_dictionary["Parameter Results"][1]

# Uniform_Calendar_k = []
# coef_a = []
# std_err_a = []
# z_a = []
# P_greater_z_a = []
# CI_Lower_a = []
# CI_Upper_a = []
# coef_b = []
# std_err_b = []
# z_b = []
# P_greater_z_b = []
# CI_Lower_b = []
# CI_Upper_b = []
# Wald_Test_Result = []

# Uniform_Calendar_k.append(int(loaded_dictionary["Uniform Calendar k"]))
# coef_a.append(float(a["coef"]))
# std_err_a.append(float(a["std err"]))
# z_a.append(float(a["z"]))
# P_greater_z_a.append(float(a["P>|z|"]))
# CI_Lower_a.append(float(a["95% CI"]["Lower"]))
# CI_Upper_a.append(float(a["95% CI"]["Upper"]))
# coef_b.append(float(b["coef"]))
# std_err_b.append(float(b["std err"]))
# z_b.append(float(b["z"]))
# P_greater_z_b.append(float(b["P>|z|"]))
# CI_Lower_b.append(float(b["95% CI"]["Lower"]))
# CI_Upper_b.append(float(b["95% CI"]["Upper"]))
# Wald_Test_Result.append(float(loaded_dictionary["Wald Test Result"]))

# df = pd.DataFrame({
#     'Uniform Calendar k':Uniform_Calendar_k,
#     'coef(a)':coef_a,
#     'std err(a)':std_err_a,
#     'z(a)':z_a,
#     'P>|z|(a)':P_greater_z_a,
#     '95% CI Lower(a)':CI_Lower_a,
#     '95% CI Upper(a)':CI_Upper_a,
#     'coef(b)':coef_b,
#     'std err(b)':std_err_b,
#     'z(b)':z_b,
#     'P>|z|(b)':P_greater_z_b,
#     '95% CI Lower(b)':CI_Lower_b,
#     '95% CI Upper(b)':CI_Upper_b,
#     'Wald Test Result':Wald_Test_Result
# })

# # int(loaded_dictionary["Uniform Calendar k"])
# # float(a["coef"])
# # float(a["std err"])
# # float(a["z"])
# # float(a["P>|z|"])
# # float(a["95% CI"]["Lower"])
# # float(a["95% CI"]["Upper"])
# # float(b["coef"])
# # float(b["std err"])
# # float(b["z"])
# # float(b["P>|z|"])
# # float(b["95% CI"]["Lower"])
# # float(b["95% CI"]["Upper"])
# # float(loaded_dictionary["Wald Test Result"])

# # Uniform_Calendar_k
# # coef_a
# # std_err_a
# # z_a
# # P_greater_z_a
# # CI_Lower_a
# # CI_Upper_a
# # coef_b
# # std_err_b
# # z_b
# # P_greater_z_b
# # CI_Lower_b
# # CI_Upper_b
# # Wald_Test_Result

# # df = pd.DataFrame({
# #     'Uniform Calendar k': [int(loaded_dictionary["Uniform Calendar k"])],
# #     'coef(a)': [float(a["coef"])],
# #     'std err(a)': [float(a["std err"])],
# #     'z(a)': [float(a["z"])],
# #     'P>|z|(a)': [float(a["P>|z|"])],
# #     '95% CI Lower(a)': [float(a["95% CI"]["Lower"])],
# #     '95% CI Upper(a)': [float(a["95% CI"]["Upper"])],
# #     'coef(b)': [float(b["coef"])],
# #     'std err(b)': [float(b["std err"])],
# #     'z(b)': [float(b["z"])],
# #     'P>|z|(b)': [float(b["P>|z|"])],
# #     '95% CI Lower(b)': [float(b["95% CI"]["Lower"])],
# #     '95% CI Upper(b)': [float(b["95% CI"]["Upper"])],
# #     'Wald Test Result': [float(loaded_dictionary["Wald Test Result"])]
# # })

# output_path = get_output_path_csv()
# df.to_csv(output_path, index=False)

# Next step:
input_dir_path = get_dir()
output_csv_path = get_output_path_csv()
tabulate_results(input_dir_path, output_csv_path)

print("All done!")