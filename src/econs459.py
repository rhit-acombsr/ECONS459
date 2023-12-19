import numpy as np
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.stats.diagnostic import het_white
from tkinter import filedialog

def get_data():
    filetypes = (("CSV files", "*.csv"), ("All files", "*.*"))
    path = filedialog.askopenfilename(filetypes=filetypes)
    print("Chose file at " + path)
    data = pd.read_csv(path)
    return data

def save_results(spacer_line_length,sumOut,tOut,white_test):
    #Save Regression Results to a text file
    file = open("Regression_Output.txt", "w")
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

def save_residuals(residuals):
    file = open("Residuals.csv", "w") 
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

def run_regression(max_lags):
    data = get_data()
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
    save_results(spacer_line_length,sumOut,tOut,white_test)

    # Write residuals to a CSV file:
    # save_residuals(residuals)

    # Plot results via matplotlib
    # plot_results(model_nw,test,predictions,residuals,Y)
    print("Done.")

max_lags = 12
run_regression(max_lags)