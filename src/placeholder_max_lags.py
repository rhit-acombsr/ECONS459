import numpy as np

# Example horizon lengths in days
horizon_lengths = [90, 180, 365]  # Extend this list as needed
# horizon_lengths = [1, 15, 30, 60, 90, 120]  # Extend this list as needed
# horizon_lengths = range(120)[1:]

# Calculate max lags using the simplified formula
# max_lags = [max(1, round(k / 30)) for k in horizon_lengths]
max_lags = [max(1, round(((k-30) / 30)*2)) for k in horizon_lengths]

# Printing max lags for each horizon
for k, lags in zip(horizon_lengths, max_lags):
    print(f"Horizon: {k} days, Max Lags: {lags}")
