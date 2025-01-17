
import pandas as pd


file_path = 'HistoricalDataSP500.csv'
df = pd.read_csv(file_path)

df_head = df.head()
df_info = df.info()
df_nulls = df.isnull().sum()

df = df.dropna()


cleaned_data = 'CleanHistoricalDataSP500.csv'
df.to_csv(cleaned_data, index=False)


