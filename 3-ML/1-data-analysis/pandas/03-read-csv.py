import pandas as pd

df = pd.read_csv("students.csv")
print(df.head())

# Handle missing values
print(df.isnull().sum())   # count missing per column
df_filled = df.fillna(0)   # fill with 0
df_dropped = df.dropna()   # drop rows with any missing value

# Save back to CSV
df.to_csv("output.csv", index=False)
