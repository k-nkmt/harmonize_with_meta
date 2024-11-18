
import pandas as pd
import json 

with open('codebook.json', 'r') as f:
    codebook = json.load(f)

# Read as DataFrame
df = pd.read_csv("2015.csv", dtype=str)
df.columns = ['var' + str(i+1) for i in range(len(df.columns))]

out = pd.DataFrame()

out["age"] = df["var19"].map(codebook["age2"]["2015"])

out["gender"] = "2015"



# Extra Code


# Output
out.to_csv("2015.csv", index=False)
