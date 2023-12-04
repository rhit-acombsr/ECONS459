import numpy as np
# import csv
import statsmodels.api as sm
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.stats.diagnostic import het_white

#Final
#data = pd.read_csv("Data - Level Model.csv")
#X = data[['$EDU', 'TAX', 'IQ', 'OIL']]
#Y = data[["GDP"]]
#y = data["GDP"]

print("good 1")

#Final
# data = pd.read_csv("PreliminaryResults.csv")
# X = data[['Futures']]
# Y = data[["Spot"]]
# y = data["Spot"]

#Basic
data = pd.read_csv("PreliminaryResults v1 - CLQ22.csv")
X = data[['ln(Ft,t-k) - ln(St-k)']]
Y = data[["ln(St) - ln(St-k)"]]
y = data["ln(St) - ln(St-k)"]
test = data["ln(Ft,t-k) - ln(St-k)"]

#Just for fun
#data = pd.read_csv("Data - Just for fun.csv")
#X = data[['EDU', 'EDU2', 'IQ', 'IQ2']]
#Y = data[["GDP"]]
#y = data["GDP"]

print("good 2")

#print(data.head(3))
#print(type(data))

#Create and evaluate model
X = sm.add_constant(X)
model = sm.OLS(Y, X).fit()
# model = sm.OLS(Y, X).fit(cov_type='HC3')
predictions = model.predict(X)
# sumOut = str(model.summary())
# fOut = str(model.f_test("const = 0, ln(Ft,t-k) - ln(St-k) = 1").summary())
tOut = str(model.t_test("const = 0, ln(Ft,t-k) - ln(St-k) = 1").summary())
residuals = np.subtract(y, predictions)

#Perform White Test
white_test = het_white(model.resid, X)

#Save Regression Results to a text file
# file = open("Regression_Summary.txt", "w")
# file = open("F-test.txt", "w")
file = open("T-test.txt", "w")

# file.write(sumOut)
# file.write('\n')
# file.write('\n')

# file.write("F-Test:")
# file.write('\n')
# file.write(fOut)
# file.write('\n')

file.write("T-Test:")
file.write('\n')
file.write(tOut)
file.write('\n')

# file.write('White Test:')
# file.write('\n')
# file.write('LM Statistic: ')
# file.write(str(white_test[0]))
# file.write('\n')
# file.write('LM-Test p-value: ')
# file.write(str(white_test[1]))
# file.write('\n')
# file.write('F-Statistic: ')
# file.write(str(white_test[2]))
# file.write('\n')
# file.write('F-Test p-value: ')
# file.write(str(white_test[3]))
file.close()

#Plot the data and regression against a variable
#sm.graphics.plot_fit(model, 1)
# name = test.name
# fig, ax1 = plt.subplots()
# ax1.scatter(test, Y, label='Observed', marker='.', color = 'b')
# ax1.scatter(test, predictions, label='Fitted', marker='.', color = 'r')
# ax1.set_xlabel(name)
# ax1.set_ylabel('ln(St) - ln(St-k)')
# ax1.set_title("CLU22")
# ax1.legend()

#Plot residuals against the fitted values to visually check for heteroskedasticity
# fig, ax2 = plt.subplots()
# ax2.scatter(predictions, residuals, marker='.', color = 'b')
# ax2.set_xlabel('Fitted Value')
# ax2.set_ylabel('Residual')
# ax2.set_title("Heteroskedasticity Test")

# plt.show()

file = open("Residuals.csv", "w") 
file.write(residuals.to_csv()) 
file.close() 

print("We gucci.")