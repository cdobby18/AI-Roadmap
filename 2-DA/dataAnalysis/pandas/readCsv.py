import pandas as pd 

df = pd.read_csv("students.csv")
print(df.head())

# SAVING DATA CSV
df.to_csv("output.csv", index=False)

# HANDLE MISSING VALUE
df.isnull()

# COUNT 
df.isnull().sum()

# FILL MISSING
df.fillna(0)

# REMOVE MISSING
df.dropna()