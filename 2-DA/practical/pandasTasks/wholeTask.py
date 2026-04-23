# TASK 1: Create a dataframe with 3 students [name, age, score]

import pandas as pd

# Create dataset
data = {
    "Name": ["Carl", "Joshua", "Coloma"],
    "Age": [23, 24, 25],
    "Score": [90, 94, 96]
}

# Convert dictionary to DataFrame
df = pd.DataFrame(data)

# Display DataFrame
print("Full DataFrame:")
print(df)

print("\nFirst 2 rows:")
print(df.head(2))

print("\nColumn Names:")
print(df.columns)

print("\nScore Column:")
print(df["Score"])

print("\nAverage Score:")
print(df["Score"].mean())