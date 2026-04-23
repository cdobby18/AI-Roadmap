"""
MINI PROJECT - STUDENT DATASET ANALYZER

"""
import pandas as pd

data = {
    "Name": ["Carl","Anna","John","Mike","Sara"],
    "Age": [23,21,25,22,24],
    "Score": [90,85,88,92,79]
}

df = pd.DataFrame(data)

print("Dataset")
print(df)

print("\nAverage Score:", df["Score"].mean())
print("Highest Score:", df["Score"].max())
print("Lowest Score:", df["Score"].min())

print("\nTop Students")
print(df[df["Score"] > 85])