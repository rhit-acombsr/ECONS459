import numpy as np
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
import os
from statsmodels.stats.diagnostic import het_white
from tkinter import filedialog

def read_csv_files():
    # Create a root window and hide it
    root = tk.Tk()
    root.withdraw()

    # Open a dialog to select a folder
    folder_path = filedialog.askdirectory()
    if not folder_path:
        return {}  # No folder was selected

    # Dictionary to store data frames
    csv_data = {}

    # Iterate through each file in the selected directory
    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            file_path = os.path.join(folder_path, file)
            try:
                csv_data[file] = pd.read_csv(file_path)
            except Exception as e:
                print(f"Error reading {file}: {e}")

    return csv_data

def get_data():
    filetypes = (("CSV files", "*.csv"), ("All files", "*.*"))
    path = filedialog.askopenfilename(filetypes=filetypes)
    print("Chose file at " + path)
    data = pd.read_csv(path)
    return data

def save_results(path_out, spacer_line_length,sumOut,tOut,white_test):
    #Save Regression Results to a text file
    file = open(path_out, "w")
    file.write((spacer_line_length*'_')+'\nSummary:\n'+(spacer_line_length*'_')+'\n')
    file.write(sumOut)
    file.write('\n\n'+(spacer_line_length*'_')+'\nT-Test:\n'+(spacer_line_length*'_')+'\n')
    file.write(tOut)
    file.write('\n\n'+(spacer_line_length*'_')+'\nWhite Test:\n'+(spacer_line_length*'_')+'\n')
    file.write('LM Statistic: ')
    file.write(str(white_test[0]))
    file.write('\n')
    file.write('LM-Test p-value: ')
    file.write(str(white_test[1]))
    file.write('\n')
    file.write('F-Statistic: ')
    file.write(str(white_test[2]))
    file.write('\n')
    file.write('F-Test p-value: ')
    file.write(str(white_test[3]))
    file.close()

def save_residuals(path_out, residuals):
    file = open(path_out, "w") 
    file.write(residuals.to_csv()) 
    file.close()

def plot_results(model,test,predictions,residuals,Y):
    # Plot the data and regression against a variable
    sm.graphics.plot_fit(model, 1)
    name = test.name
    fig, ax1 = plt.subplots()
    ax1.scatter(test, Y, label='Observed', marker='.', color = 'b')
    ax1.scatter(test, predictions, label='Fitted', marker='.', color = 'r')
    ax1.set_xlabel(name)
    ax1.set_ylabel('ln(St) - ln(St-k)')
    # ax1.set_title("CLU22")
    ax1.legend()

    # Plot residuals against the fitted values to visually check for heteroskedasticity
    fig, ax2 = plt.subplots()
    ax2.scatter(predictions, residuals, marker='.', color = 'b')
    ax2.set_xlabel('Fitted Value')
    ax2.set_ylabel('Residual')
    ax2.set_title("Heteroskedasticity Test")

    # Display plots
    plt.show()

def run_regression(data, max_lags):
    
    X = data[['ln(Ft,t-k) - ln(St-k)']]
    Y = data[["ln(St) - ln(St-k)"]]
    y = data["ln(St) - ln(St-k)"]
    test = data["ln(Ft,t-k) - ln(St-k)"]

    #Create and evaluate model
    X = sm.add_constant(X)
    model = sm.OLS(Y, X)
    model_default = model.fit()
    model_HC3 = model.fit()
    model_nw = model.fit(cov_type='HAC', cov_kwds={'maxlags': max_lags})

    predictions = model_nw.predict(X)
    sumOut = str(model_nw.summary())
    tOut = str(model_nw.t_test("const = 0, ln(Ft,t-k) - ln(St-k) = 1").summary())
    residuals = np.subtract(y, predictions)

    #Perform White Test:
    white_test = het_white(model_nw.resid, X)

    #Save Regression Results to a text file:
    spacer_line_length = 90
    save_results("Regression_Output.txt", spacer_line_length,sumOut,tOut,white_test)

    # Write residuals to a CSV file:
    # save_residuals("Residuals.csv", residuals)

    # Plot results via matplotlib
    # plot_results(model_nw,test,predictions,residuals,Y)
    print("Done.")

def create_regression_model(data, max_lags):
    
    X = data[['ln(Ft,t-k) - ln(St-k)']]
    Y = data[["ln(St) - ln(St-k)"]]
    y = data["ln(St) - ln(St-k)"]
    test = data["ln(Ft,t-k) - ln(St-k)"]

    #Create and evaluate model
    X = sm.add_constant(X)
    model = sm.OLS(Y, X)
    model_nw = model.fit(cov_type='HAC', cov_kwds={'maxlags': max_lags})
    return model_nw

def run_regression_and_test_hypotheses(data, max_lags, output_file_path):
    # Prepare the independent and dependent variables
    X = data[['ln(Ft,t-k) - ln(St-k)']]
    y = data['ln(St) - ln(St-k)']

    # Add a constant to the model for the intercept
    X = sm.add_constant(X)

    # Fit the model using OLS with HAC standard errors
    model = sm.OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags': max_lags})

    # Perform Wald tests for the specific hypotheses
    wald_test_results = model.t_test("const = 0, ln(Ft,t-k) - ln(St-k) = 1")

    # Save the regression summary and Wald test results to a text file
    with open(output_file_path, 'w') as output_file:
        output_file.write(model.summary().as_text())
        output_file.write("\n\nWald Test Results:\n")
        output_file.write(wald_test_results.summary().as_text())

    print("Regression analysis and hypothesis testing complete. Results saved to:", output_file_path)

# Example usage:
# data = your_dataframe_here
# max_lags = your_max_lags_value_here
# output_file_path = "Regression_Output.txt"
# run_regression_and_test_hypotheses(data, max_lags, output_file_path)

def run_regression_no_constant_and_test(data, max_lags, output_file_path):
    # Prepare the independent variable
    X = data[['ln(Ft,t-k) - ln(St-k)']]
    y = data['ln(St) - ln(St-k)']

    # Note: We're not adding a constant to the model, fitting through the origin

    # Fit the model using OLS with HAC standard errors, without adding a constant
    model = sm.OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags': max_lags})

    # Perform a Wald test for the hypothesis that the coefficient is equal to one
    # Note: The syntax "[ln(Ft,t-k) - ln(St-k)]=1" assumes the variable name matches; adjust as necessary
    wald_test_results = model.t_test("ln(Ft,t-k) - ln(St-k)=1")

    # Save the regression summary and Wald test results to a text file
    with open(output_file_path, 'w') as output_file:
        output_file.write(model.summary().as_text())
        output_file.write("\n\nWald Test Results:\n")
        output_file.write(wald_test_results.summary().as_text())

    print("Regression analysis (without constant) and hypothesis testing complete. Results saved to:", output_file_path)

# Example usage:
# data = your_dataframe_here
# max_lags = your_max_lags_value_here
# output_file_path = "Regression_Output_No_Constant.txt"
# run_regression_no_constant_and_test(data, max_lags, output_file_path)

def run_regression_with_dynamic_lags_and_wald_test(data, K, output_file_path):
    # Calculate max lags based on the paper's formula
    max_lags = 2 * (K - 1)
    
    # Prepare the independent variable (without adding a constant)
    X = data[['ln(Ft,t-k) - ln(St-k)']]
    y = data['ln(St) - ln(St-k)']

    # Fit the model using OLS with HAC standard errors, based on the dynamic max lags
    model = sm.OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags': max_lags})

    # Perform a Wald test for the hypothesis that the coefficient is equal to one
    wald_test_result = model.t_test(f"ln(Ft,t-k) - ln(St-k)=1")

    # Extract the Wald test statistic
    wald_statistic = wald_test_result.statistic[0][0]

    # Save the regression summary and Wald test statistic to a text file
    with open(output_file_path, 'w') as output_file:
        output_file.write(model.summary().as_text())
        output_file.write(f"\n\nWald Test Statistic: {wald_statistic}\n")

    print("Regression analysis and Wald test complete. Results saved to:", output_file_path)

# Example usage:
# data = your_dataframe_here
# K = your_K_value_here
# output_file_path = "Regression_Output_With_Dynamic_Lags_And_Wald_Test.txt"
# run_regression_with_dynamic_lags_and_wald_test(data, K, output_file_path)

def run_regression_with_constant_and_calculate_wald(data, K, output_file_path):
    # Prepare the independent variable and add a constant
    X = sm.add_constant(data[['ln(Ft,t-k) - ln(St-k)']])
    y = data['ln(St) - ln(St-k)']
    
    # Calculate max_lags as per the paper's methodology
    max_lags = 2 * (K - 1)

    # Fit the model using OLS with HAC standard errors
    model = sm.OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags': max_lags})

    # Use the parameter name from the model summary for the Wald test constraint
    # This example assumes your independent variable is exactly named 'ln(Ft,t-k) - ln(St-k)'
    # Adjust the string as needed to match the model summary
    # constraint = 'ln(Ft,t-k) - ln(St-k) = 1'
    constraint = 'const = 0'
    
    # Calculate the Wald test statistic for the hypothesis of interest
    wald_result = model.wald_test(constraint, use_f=False)

    # Save the regression summary and Wald test result to a text file
    with open(output_file_path, 'w') as output_file:
        output_file.write(model.summary().as_text())
        output_file.write("\n\nWald Test Result:\n")
        output_file.write(str(wald_result))

    print("Regression analysis with constant and Wald statistic calculation complete. Results saved to:", output_file_path)

# Example usage:
# K = number_of_months
# data = your_dataframe_here
# output_file_path = "Regression_Output_With_Wald.txt"
# run_regression_with_constant_and_calculate_wald(data, K, output_file_path)

def run_regression_and_wald_test(data, K, output_file_path):
    X = data[['ln(Ft,t-k) - ln(St-k)']]  # Independent variable
    y = data['ln(St) - ln(St-k)']  # Dependent variable
    X = sm.add_constant(X)  # Add a constant term for the intercept
    
    # Fit the OLS model with HAC (Newey-West) standard errors
    model = sm.OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags': 2*(K-1)})
    
    # Define the joint hypothesis for Wald test: a=0 and b=1
    hypothesis = '(const = 0), (ln(Ft,t-k) - ln(St-k) = 1)'
    
    # Perform the Wald test
    wald_test_result = model.wald_test(hypothesis)
    
    # Save results
    with open(output_file_path, 'w') as file:
        file.write(model.summary().as_text())
        file.write("\n\nWald Test Result (p-value for joint hypothesis a=0 and b=1):\n")
        file.write(str(wald_test_result.pvalue))
    
    print("Analysis complete. Results saved to:", output_file_path)

# Example usage
# run_regression_and_wald_test(data, K, "output.txt")


def get_output_results_path():
    filetypes = (("Text files", "*.txt"), ("All files", "*.*"))
    path = filedialog.asksaveasfilename(filetypes=filetypes)
    return path

def k_to_max_lags(k):
    return max(1, round(((k-30) / 30)*2))

k = 63
max_lags = k_to_max_lags(k)
# max_lags = 2*(k-1)
# max_lags = 1
data = get_data()
# data = pd.read_csv("C:\\Users\\acombsr\\OneDrive - Rose-Hulman Institute of Technology\\Documents\\GitHub\\ECONS459\\data\\reproducing_key_paper\\_with oil_1 as spot\\oil3\\m-1\\Reproduction of Results - Reproduced oil_3 h=m01 spot=oil_1.csv")
# data = pd.read_csv("C:\\Users\\acombsr\\OneDrive - Rose-Hulman Institute of Technology\\Documents\\GitHub\\ECONS459\\data\\reproducing_key_paper\\_with oil_1 as spot\\oil6\\m-1\\Reproduction of Results - Reproduced oil_6 with oil_1 as Spot and h=m-1.csv")
# data = pd.read_csv("C:\\Users\\acombsr\\OneDrive - Rose-Hulman Institute of Technology\\Documents\\GitHub\\ECONS459\\data\\reproducing_key_paper\\_with oil_1 as spot\\oil12\\m-1\\Reproduction of Results - Reproduced oil_12 with oil1 as Spot and h=m-1.csv")

output_results_path = get_output_results_path()
# output_results_path = "C:\\Users\\acombsr\\OneDrive - Rose-Hulman Institute of Technology\\Documents\\GitHub\\ECONS459\\results\\01-09-24\\Regression_Output-oil3_m-1_oil_1_as_spot_minimalist_no_constant_maxlags_"+str(max_lags)+".txt"
# output_results_path = "C:\\Users\\acombsr\\OneDrive - Rose-Hulman Institute of Technology\\Documents\\GitHub\\ECONS459\\results\\01-09-24\\Regression_Output-oil6_m-1_oil_1_as_spot_minimalist_no_constant_maxlags_"+str(max_lags)+".txt"

# output_results_path = "C:\\Users\\acombsr\\OneDrive - Rose-Hulman Institute of Technology\\Documents\\GitHub\\ECONS459\\results\\01-09-24\\Regression_Output-oil3_m-1_oil_1_as_spot_minimalist_maxlags_"+str(max_lags)+".txt"
# output_results_path = "C:\\Users\\acombsr\\OneDrive - Rose-Hulman Institute of Technology\\Documents\\GitHub\\ECONS459\\results\\01-09-24\\Regression_Output-oil6_m-1_oil_1_as_spot_minimalist_maxlags_"+str(max_lags)+".txt"
# output_results_path = "C:\\Users\\acombsr\\OneDrive - Rose-Hulman Institute of Technology\\Documents\\GitHub\\ECONS459\\results\\01-09-24\\Regression_Output-oil12_m-1_oil_1_as_spot_minimalist_maxlags_"+str(max_lags)+".txt"

# output_results_path = "C:\\Users\\acombsr\\OneDrive - Rose-Hulman Institute of Technology\\Documents\\GitHub\\ECONS459\\results\\01-09-24\\Regression_Output-oil3_m-1_oil_1_as_spot_wald_maxlags_"+str(max_lags)+".txt"
# output_results_path = "C:\\Users\\acombsr\\OneDrive - Rose-Hulman Institute of Technology\\Documents\\GitHub\\ECONS459\\results\\01-09-24\\Regression_Output-oil6_m-1_oil_1_as_spot_wald_maxlags_"+str(max_lags)+".txt"
# output_results_path = "C:\\Users\\acombsr\\OneDrive - Rose-Hulman Institute of Technology\\Documents\\GitHub\\ECONS459\\results\\01-09-24\\Regression_Output-oil12_m-1_oil_1_as_spot_wald_maxlags_"+str(max_lags)+".txt"

# run_regression_and_test_hypotheses(data, max_lags, output_results_path)
# run_regression_no_constant_and_test(data, max_lags, output_results_path)
# run_regression_with_dynamic_lags_and_wald_test(data, k, output_results_path)
# run_regression_with_constant_and_calculate_wald(data, k, output_results_path)
run_regression_and_wald_test(data, k, output_results_path)


# k = 63
# max_lags = 2*(k-1)
# data = get_data()
# run_regression(data, max_lags)

# datafiles_dict = read_csv_files()

# print(str(type(datafiles_dict))) #<class 'dict'>

# # key type = <class 'str'>
# # key = Reproduction of Results - Reproduced oil_12 horizon = m-1.csv
# # value type = <class 'pandas.core.frame.DataFrame'>
# for key in datafiles_dict.keys():
#     print("key type = " + str(type(key)))
#     print("key = " + str(key))
#     print("value type = " + str(type(datafiles_dict[key])))

# for value in datafiles_dict.values():
#     model = create_regression_model(value, 12)
#     # print(str(type(model))) # <class 'statsmodels.regression.linear_model.RegressionResultsWrapper'>
#     # print(str(type(model.summary()))) # <class 'statsmodels.iolib.summary.Summary'>
#     # print(str(model.summary())) # 
#     model_summary = model.summary()
#     # model_summary_csv = model_summary.as_csv()
#     # print(model_summary_csv) # 
#     # print(str(model.params)) # output estimates!
#     # print(str(type(model.params))) # <class 'pandas.core.series.Series'>
#     # print(str(type(model.params.array))) # <class 'pandas.core.arrays.numpy_.NumpyExtensionArray'>
#     # print(str(type(model.params.array.tolist()))) # <class 'list'>
#     # print(str(model.params.array.tolist())) # [0.07732635592781496, 0.7412839707406351] <- alpha & beta!
#     # print(str(type(model.bse))) # <class 'pandas.core.series.Series'>
#     print(str(model.bse.array.tolist())) # [0.045315039486414375, 0.2933164407833197] <- stderr for alpha & beta!

