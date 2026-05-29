import pandas as pd

data = {
    "Name": ["Carl", "Joshua", "Coloma"],
    "Age": [23, 24, 25],
    "Score": [90, 94, 96]
}

df = pd.DataFrame(data)
print(df)

# Viewing data
print(df.head())   # first rows
print(df.tail())   # last rows

# Info and stats
df.info()
print(df.describe())

# Accessing columns and rows
print(df["Name"])
print(df.loc[1])     # by label/index
print(df.iloc[0])    # by integer position

# Filtering rows
print(df[df["Score"] > 90])

# Adding a new column
df["Passed"] = df["Score"] > 85
print(df)
