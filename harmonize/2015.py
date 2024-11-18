import pandas as pd
import json

df = pd.read_csv('jp_data/2015kokucho.csv', header=None, dtype=str,encoding="cp932")
df.columns = ['var' + str(i+1) for i in range(len(df.columns))]

with open('code/dict.json', 'r') as f:
    codebook = json.load(f)

out = pd.DataFrame()

out["country"] = ""
out["year"] = ""
out["sample"] = ""

out["pref_jp"] =df["var4"]
out["region_jp"] = df["var4"].map(codebook["region_jp"]["japan2015"])
out["munic_jp"] = df["var4"] + df["var5"]

out["serial"] = df["var7"]
out["pernum"] = df["var8"]
out["gq"] = df["var9"].map(codebook["gq"]["japan2015"])
out["bldgtype"] = df["var10"].map(codebook["bldgtype"]["japan2015"])
out["stories"] = df["var11"].map(codebook["stories"]["japan2015"])
out["storyhh"] = df["var12"].map(codebook["storyhh"]["japan2015"])
out["ownership"] = df["var13"].map(codebook["ownership"]["japan2015"])

out["persons"] = df["var14"]
out["hhtype"] = df["var15"].map(codebook["hhtype"]["japan2015"])
out["multigen"] = df["var16"].map(codebook["multigen"]["japan2015"])

out["relate"] = df["var17"].map(codebook["relate"]["japan2015"])
out["related"] = df["var17"].map(codebook["related"]["japan2015"])
out["sex"] = df["var18"].map(codebook["sex"]["japan2015"])
out["age"] = df["var19"].map(codebook["age"]["japan2015"])
out["age2"] = df["var19"].map(codebook["age2"]["japan2015"])
out["marst"] = df["var20"].map(codebook["marst"]["japan2015"])
out["marstd"] = df["var20"].map(codebook["marstd"]["japan2015"])
out["citizen"] = df["var21"].map(codebook["citizen"]["japan2015"])
out["migyrs2"] = df["var22"].map(codebook["migyrs2"]["japan2015"])
out["migrate5"] = df["var23"].map(codebook["migrate5"]["japan2015"])
out["empstat"] = df["var24"].map(codebook["empstat"]["japan2015"])
out["empstatd"] = df["var24"].map(codebook["empstatd"]["japan2015"])
out["labforce"] = df["var24"].map(codebook["labforce"]["japan2015"])

out["placework"] = df["var25"].map(codebook["placework"]["japan2015"])
out["classwk"] = df["var26"].map(codebook["classwk"]["japan2015"])
out["classwkd"] = df["var26"].map(codebook["classwkd"]["japan2015"])
out["indgen"] = df["var27"].map(codebook["indgen"]["japan2015"])
out["ind_jp"] = df["var27"].map(codebook["ind_jp"]["japan2015"])
out["occisco"] = df["var28"].map(codebook["occisco"]["japan2015"])
out["occ_jp"] = df["var28"].map(codebook["occ_jp"]["japan2015"])

# 個別対応
out["country"] = "392"
out["year"] = "2015"
out["sample"] = "392201501"

# if (age < 4, under 15) labforce = 9
out.loc[out['age'].isin(['1', '2', '3']), "labforce"] = "9"

# 出力
out.to_csv("ipums_data/2015kokucho_ipums.csv", index=False)