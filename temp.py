import pandas as pd

data=pd.read_csv('FinalLog.csv')

# d=data.iloc[0:0]
# print(d)
# z=data.columns
# print(z)
names = []
for x in data.columns:
    if x=='email' or x=='time' or x=='date' or x==' ':
        names.append(x)
print(names)
df_b = pd.DataFrame(columns=names)
print(df_b)
df_b.to_csv('FinalLog.csv')