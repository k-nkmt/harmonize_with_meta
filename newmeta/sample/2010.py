
import pandas as pd
import json 

with open('codebook.json', 'r') as f:
    codebook = json.load(f)

# Read as DataFrame
df = pd.read_csv("2010.csv", dtype=str)
df.columns = ['var' + str(i+1) for i in range(len(df.columns))]

out = pd.DataFrame()

out["age"] = df["var20"].map(codebook["age2"]["2010"])

out["gender"] = "2010"



# Extra Code


# Output
out.to_csv("2010.csv", index=False)
