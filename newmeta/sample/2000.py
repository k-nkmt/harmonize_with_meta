
import pandas as pd
import json 

with open('codebook.json', 'r') as f:
    codebook = json.load(f)

# Read as DataFrame
df = pd.read_csv("2000.csv", dtype=str)
df.columns = ['var' + str(i+1) for i in range(len(df.columns))]

out = pd.DataFrame()

out["age"] = df["var21"].map(codebook["age2"]["2000"])
out["inctype"] = df["var15"]
out["gender"] = "2000"



# Extra Code


# Output
out.to_csv("2000.csv", index=False)
