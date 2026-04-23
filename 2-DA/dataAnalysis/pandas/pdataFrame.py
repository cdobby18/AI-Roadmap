import pandas as pd

data = {
    "Name": ["Carl","Joshua","Coloma"],
    "Age": [23,24,25],
    "Score": [90,94,96]
}

df = pd.DataFrame(data)
print(df)

# VIEWING OF DATA
print(df.head()) #first row
print(df.tail()) #last row

# BASIC INFORMATION
df.info()
df.describe()

# ACCESSING COLUMNS & ROWS
print(df["Name"])
print(df.loc[1])

# FILTERING DATA
print(df.loc[1])

# ADDING NEW COLUMN
df["Passed"] = df["Score"] > 85

print(df)