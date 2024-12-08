
# Ensure the correct path for the CSV
import pandas as pd
df = pd.read_csv("heart.csv")  # Use relative path if necessary

import os

# Print the current working directory
print("Current working directory:", os.getcwd())
print(df.head())