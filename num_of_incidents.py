import pandas as pd

df = pd.read_csv('incidents.csv')

# create empty dataframe with columns
columns = ['Date', 'Num']

arr = []
for a in list(df['rpt']):
    arr.append(a.split(' ')[1])

freq = {} 
for items in arr: 
    freq[items] = arr.count(items)

print(freq)
num_inc_df = pd.DataFrame(freq.items(), columns=columns)
print(num_inc_df)
num_inc_df.to_csv('num_inc.csv')