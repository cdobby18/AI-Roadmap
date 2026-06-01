import pandas as pd

df = pd.read_csv('orders.csv')
print(df)

df.groupby('Country')["Price"].sum()
print(df.groupby('Country')["Price"].sum())