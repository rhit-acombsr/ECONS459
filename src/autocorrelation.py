from statsmodels.tsa.stattools import acf

# Calculate autocorrelation for lag 1
lag_1_acf = acf(residuals_df['ui^'], nlags=1, fft=False)

# Extract the autocorrelation value for lag 1
lag_1_autocorrelation = lag_1_acf[1]

lag_1_autocorrelation
