import numpy as np 
import pandas as pd 

data_gasoline = pd.read_csv(r"C:/Users/behri/OneDrive/Desktop/Master LSE/Essay/Ideas/Pepsi Coke/GASREGW.csv")
data = pd.read_csv(r"C:/Users/behri/OneDrive/Desktop/Master LSE/Essay/Ideas/Pepsi Coke/final_data.csv")

## INSTRUMENT VARIABLES ## 

week = 146
for i, idx in enumerate(data_gasoline.index): 
    data_gasoline.loc[idx, "WEEK"] = week + i
    
for idx in range(2, len(data_gasoline["WEEK"])): 
    data_gasoline.loc[idx, "pct_change"] = (data_gasoline.loc[idx, "GASREGW"] - data_gasoline.loc[idx-1, "GASREGW"]) / (data_gasoline.loc[idx-1, "GASREGW"])

# Assume linear relationship between trends if there is no change in order not to lose the variation across those weeks
for i in range(1, len(data_gasoline["WEEK"])):
    if data_gasoline.loc[i,"pct_change"] == 0:
        data_gasoline.loc[i, "pct_change"] = (data_gasoline.loc[i+1, "pct_change"] + data_gasoline.loc[i-1, "pct_change"]) / 2

data = data.merge(data_gasoline, on = "WEEK", how = "left")
data["pct_change"] = data["pct_change"].fillna(0)
