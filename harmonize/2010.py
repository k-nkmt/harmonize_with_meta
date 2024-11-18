import pandas as pd
import json

df = pd.read_csv('jp_data/2010kokucho.csv', header=None, dtype=str,encoding="cp932")
df.columns = ['var' + str(i+1) for i in range(len(df.columns))]

with open('code/dict.json', 'r') as f:
    codebook = json.load(f)

out = pd.DataFrame()

out["country"] = ""
out["year"] = ""
out["sample"] = ""

out["pref_jp"] =df["var4"]
out["region_jp"] = df["var4"].map(codebook["region_jp"]["japan2010"])
out["munic_jp"] = df["var4"] + df["var5"]

out["serial"] = df["var7"]
out["pernum"] = df["var8"]
out["gq"] = df["var9"].map(codebook["gq"]["japan2010"])
out["bldgtype"] = df["var10"].map(codebook["bldgtype"]["japan2010"])
out["stories"] = df["var11"].map(codebook["stories"]["japan2010"])
out["storyhh"] = df["var12"].map(codebook["storyhh"]["japan2010"])
out["ownership"] = df["var13"].map(codebook["ownership"]["japan2010"])
out["livearea"] = df["var14"].map(codebook["livearea"]["japan2010"])

out["persons"] = df["var15"]
out["hhtype"] = df["var16"].map(codebook["hhtype"]["japan2010"])
out["multigen"] = df["var17"].map(codebook["multigen"]["japan2010"])

out["relate"] = df["var18"].map(codebook["relate"]["japan2010"])
out["related"] = df["var18"].map(codebook["related"]["japan2010"])
out["sex"] = df["var19"].map(codebook["sex"]["japan2010"])
out["age"] = df["var20"].map(codebook["age"]["japan2010"])
out["age2"] = df["var20"].map(codebook["age2"]["japan2010"])
out["marst"] = df["var21"].map(codebook["marst"]["japan2010"])
out["marstd"] = df["var21"].map(codebook["marstd"]["japan2010"])
out["citizen"] = df["var22"].map(codebook["citizen"]["japan2010"])
out["migyrs2"] = df["var23"].map(codebook["migyrs2"]["japan2010"])
out["migrate5"] = df["var24"].map(codebook["migrate5"]["japan2010"])

out["school"] = df["var25"].map(codebook["school"]["japan2010"])
out["educ_jp"] = df["var26"].map(codebook["educ_jp"]["japan2010"])
out["edattain"] = df["var26"].map(codebook["edattain"]["japan2010"])

out["empstat"] = df["var27"].map(codebook["empstat"]["japan2010"])
out["empstatd"] = df["var27"].map(codebook["empstatd"]["japan2010"])
out["labforce"] = df["var27"].map(codebook["labforce"]["japan2010"])

out["trnwrk"] = df["var28"].map(codebook["trnwrk"]["japan2010"])
out["placework"] = df["var29"].map(codebook["placework"]["japan2010"])
out["classwk"] = df["var30"].map(codebook["classwk"]["japan2010"])
out["classwkd"] = df["var30"].map(codebook["classwkd"]["japan2010"])
out["indgen"] = df["var31"].map(codebook["indgen"]["japan2010"])
out["ind_jp"] = df["var31"].map(codebook["ind_jp"]["japan2010"])
out["occisco"] = df["var32"].map(codebook["occisco"]["japan2010"])
out["occ_jp"] = df["var32"].map(codebook["occ_jp"]["japan2010"])

# 個別対応
out["country"] = "392"
out["year"] = "2010"
out["sample"] = "392201001"

# if (age < 4, under 15) labforce = 9
out.loc[out['age'].isin(['1', '2', '3']), "labforce"] = "9"

# if (school_type = 7 and age = 1) school = 2. 
out.loc[(df['var26']=='7') & (df["var20"] == '01'), "school"] = "2"

# If (school_attainment = 2 and student = 1) edattain = 221
# If (school_attainment = 3 and student = 1) edattain = 311
# If (school_attainment = 4 and student = 1) edattain = 312
out.loc[(df["var26"] == '2') & (df["var25"] == '1'), 'edattain'] = '221'
out.loc[(df["var26"] == '3') & (df["var25"] == '1'), 'edattain'] = '311'
out.loc[(df["var26"] == '4') & (df["var25"] == '1'), 'edattain'] = '312'

# 出力
out.to_csv("ipums_data/2010kokucho_ipums.csv", index=False)