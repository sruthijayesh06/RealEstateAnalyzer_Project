import pandas as pd

df = pd.read_csv('data/outputs/analyzed_properties.csv')
print('Unique cities:')
print(df['city'].unique())
print(f'\nTotal properties: {len(df)}')
print(f'\nPune count: {len(df[df["city"].str.lower() == "pune"])}')
print(f'\nColumn names: {df.columns.tolist()}')
print(f'\nFirst few rows:')
print(df.head(3))
