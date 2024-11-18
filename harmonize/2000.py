import pandas as pd
import json

df = pd.read_csv('jp_data/2000kokucho.csv', header=None, dtype=str,encoding="cp932")
df.columns = ['var' + str(i+1) for i in range(len(df.columns))]

with open('code/dict.json', 'r') as f:
    codebook = json.load(f)

out = pd.DataFrame()

out["country"] = ""
out["year"] = ""
out["sample"] = ""

out["pref_jp"] =df["var4"]
out["region_jp"] = df["var4"].map(codebook["region_jp"]["japan2000"])
out["munic_jp"] = df["var4"] + df["var5"]

out["serial"] = df["var7"]
out["pernum"] = df["var8"]
out["gq"] = df["var9"].map(codebook["gq"]["japan2000"])
out["bldgtype"] = df["var10"].map(codebook["bldgtype"]["japan2000"])
out["stories"] = df["var11"].map(codebook["stories"]["japan2000"])
out["storyhh"] = df["var12"].map(codebook["storyhh"]["japan2000"])
out["ownership"] = df["var13"].map(codebook["ownership"]["japan2000"])
out["livearea"] = df["var14"].map(codebook["livearea"]["japan2000"])
out["inctype"] = df["var15"].map(codebook["inctype"]["japan2000"])

out["persons"] = df["var16"]
out["hhtype"] = df["var17"].map(codebook["hhtype"]["japan2000"])
out["multigen"] = df["var18"].map(codebook["multigen"]["japan2000"])

out["relate"] = df["var19"].map(codebook["relate"]["japan2000"])
out["related"] = df["var19"].map(codebook["related"]["japan2000"])
out["sex"] = df["var20"].map(codebook["sex"]["japan2000"])
out["age"] = df["var21"].map(codebook["age"]["japan2000"])
out["age2"] = df["var21"].map(codebook["age2"]["japan2000"])
out["marst"] = df["var22"].map(codebook["marst"]["japan2000"])
out["marstd"] = df["var22"].map(codebook["marstd"]["japan2000"])
out["citizen"] = df["var23"].map(codebook["citizen"]["japan2000"])
out["migyrs2"] = df["var24"].map(codebook["migyrs2"]["japan2000"])
out["migrate5"] = df["var25"].map(codebook["migrate5"]["japan2000"])

out["school"] = df["var26"].map(codebook["school"]["japan2000"])
out["educ_jp"] = df["var27"].map(codebook["educ_jp"]["japan2000"])
out["edattain"] = df["var27"].map(codebook["edattain"]["japan2000"])

out["empstat"] = df["var28"].map(codebook["empstat"]["japan2000"])
out["empstatd"] = df["var28"].map(codebook["empstatd"]["japan2000"])
out["labforce"] = df["var28"].map(codebook["labforce"]["japan2000"])
out["hrswork1"] = df["var29"].map(codebook["hrswork1"]["japan2000"])

out["trnwrk"] = df["var34"].map(codebook["trnwrk"]["japan2000"])
out["placework"] = df["var35"].map(codebook["placework"]["japan2000"])
out["classwk"] = df["var36"].map(codebook["classwk"]["japan2000"])
out["classwkd"] = df["var36"].map(codebook["classwkd"]["japan2000"])
out["indgen"] = df["var37"].map(codebook["indgen"]["japan2000"])
out["ind_jp"] = df["var37"].map(codebook["ind_jp"]["japan2000"])
out["occisco"] = df["var38"].map(codebook["occisco"]["japan2000"])
out["occ_jp"] = df["var38"].map(codebook["occ_jp"]["japan2000"])

# 個別対応
out["country"] = "392"
out["year"] = "2000"
out["sample"] = "392201001"

# if (age < 4, under 15) labforce = 9
out.loc[out['age'].isin(['1', '2', '3']), "labforce"] = "9"

# if (school_type = 7 and age = 1) school = 2. 
out.loc[(df["var27"]=='7') & (df["var21"] == '1'), "school"] = "2"

# If (school_attainment = 2 and student = 1) edattain = 221
# If (school_attainment = 3 and student = 1) edattain = 311
# If (school_attainment = 4 and student = 1) edattain = 312
out.loc[(df["var27"] == '2') & (df["var26"] == '1'), 'edattain'] = '221'
out.loc[(df["var27"] == '3') & (df["var26"] == '1'), 'edattain'] = '311'
out.loc[(df["var27"] == '4') & (df["var26"] == '1'), 'edattain'] = '312'

# 出力

out.to_csv("ipums_data/2000kokucho_ipums.csv", index=False)