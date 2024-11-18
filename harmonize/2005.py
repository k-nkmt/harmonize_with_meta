import pandas as pd
import json

df = pd.read_csv('jp_data/2005kokucho.csv', header=None, dtype=str,encoding="cp932")
df.columns = ['var' + str(i+1) for i in range(len(df.columns))]

with open('code/dict.json', 'r') as f:
    codebook = json.load(f)

out = pd.DataFrame()

out["country"] = ""
out["year"] = ""
out["sample"] = ""

out["pref_jp"] =df["var4"]
out["region_jp"] = df["var4"].map(codebook["region_jp"]["japan2005"])
out["munic_jp"] = df["var4"] + df["var5"]

out["serial"] = df["var7"]
out["pernum"] = df["var8"]
out["gq"] = df["var9"].map(codebook["gq"]["japan2005"])
out["bldgtype"] = df["var10"].map(codebook["bldgtype"]["japan2005"])
out["stories"] = df["var11"].map(codebook["stories"]["japan2005"])
out["storyhh"] = df["var12"].map(codebook["storyhh"]["japan2005"])
out["ownership"] = df["var13"].map(codebook["ownership"]["japan2005"])
out["livearea"] = df["var14"].map(codebook["livearea"]["japan2005"])

out["persons"] = df["var15"]
out["hhtype"] = df["var16"].map(codebook["hhtype"]["japan2005"])
out["multigen"] = df["var17"].map(codebook["multigen"]["japan2005"])

out["relate"] = df["var18"].map(codebook["relate"]["japan2005"])
out["related"] = df["var18"].map(codebook["related"]["japan2005"])
out["sex"] = df["var19"].map(codebook["sex"]["japan2005"])
out["age"] = df["var20"].map(codebook["age"]["japan2005"])
out["age2"] = df["var20"].map(codebook["age2"]["japan2005"])
out["marst"] = df["var21"].map(codebook["marst"]["japan2005"])
out["marstd"] = df["var21"].map(codebook["marstd"]["japan2005"])
out["citizen"] = df["var22"].map(codebook["citizen"]["japan2005"])

out["empstat"] = df["var23"].map(codebook["empstat"]["japan2005"])
out["empstatd"] = df["var23"].map(codebook["empstatd"]["japan2005"])
out["labforce"] = df["var23"].map(codebook["labforce"]["japan2005"])
out["hrswork1"] = df["var24"].map(codebook["hrswork1"]["japan2005"])

out["placework"] = df["var30"].map(codebook["placework"]["japan2005"])
out["classwk"] = df["var31"].map(codebook["classwk"]["japan2005"])
out["classwkd"] = df["var31"].map(codebook["classwkd"]["japan2005"])
out["indgen"] = df["var32"].map(codebook["indgen"]["japan2005"])
out["ind_jp"] = df["var32"].map(codebook["ind_jp"]["japan2005"])
out["occisco"] = df["var33"].map(codebook["occisco"]["japan2005"])
out["occ_jp"] = df["var33"].map(codebook["occ_jp"]["japan2005"])

# 個別対応
out["country"] = "392"
out["year"] = "2005"
out["sample"] = "392201001"

# if (age < 4, under 15) labforce = 9
out.loc[out['age'].isin(['1', '2', '3']), "labforce"] = "9"

# 出力
out.to_csv("ipums_data/2005kokucho_ipums.csv", index=False)