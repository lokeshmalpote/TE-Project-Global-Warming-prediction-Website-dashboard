import pandas as pd
df = pd.read_csv('data.csv',sep='\s+',header=None)
df.to_csv('data_out.csv',header=None)