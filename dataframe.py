import pandas as pd

d = {'habit name': ["Sport", "Sport", "Sleep"], 'Status': ["closed", "open", "open"], 'Due': ["11-01-2024", "01-02-2024", "04-03-2024"]}
df = pd.DataFrame(data=d)
blub = df[(df["habit name"] == "Sport") & (df["Status"] == "open")]
print(blub.iloc[0,2])