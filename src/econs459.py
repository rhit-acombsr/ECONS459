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


# k = 12
# max_lags = 2*(k-1)
# data = get_data()
# run_regression(data, max_lags)

datafiles_dict = read_csv_files()

# print(str(type(datafiles_dict))) #<class 'dict'>

# # key type = <class 'str'>
# # key = Reproduction of Results - Reproduced oil_12 horizon = m-1.csv
# # value type = <class 'pandas.core.frame.DataFrame'>
# for key in datafiles_dict.keys():
#     print("key type = " + str(type(key)))
#     print("key = " + str(key))
#     print("value type = " + str(type(datafiles_dict[key])))

for value in datafiles_dict.values():
    model = create_regression_model(value, 12)
    # print(str(type(model))) # <class 'statsmodels.regression.linear_model.RegressionResultsWrapper'>
    # print(str(type(model.summary()))) # <class 'statsmodels.iolib.summary.Summary'>
    # print(str(model.summary())) # 
    model_summary = model.summary()
    # model_summary_csv = model_summary.as_csv()
    # print(model_summary_csv) # 
    # print(str(model.params)) # output estimates!
    # print(str(type(model.params))) # <class 'pandas.core.series.Series'>
    # print(str(type(model.params.array))) # <class 'pandas.core.arrays.numpy_.NumpyExtensionArray'>
    # print(str(type(model.params.array.tolist()))) # <class 'list'>
    # print(str(model.params.array.tolist())) # [0.07732635592781496, 0.7412839707406351] <- alpha & beta!
    # print(str(type(model.bse))) # <class 'pandas.core.series.Series'>
    print(str(model.bse.array.tolist())) # [0.045315039486414375, 0.2933164407833197] <- stderr for alpha & beta!