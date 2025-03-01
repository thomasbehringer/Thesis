import numpy as np 
import pandas as pd 

data_gasoline = pd.read_csv(r"C:/Users/behri/OneDrive/Desktop/Master LSE/Essay/Ideas/Pepsi Coke/GASREGW.csv")
data = pd.read_csv(r"C:/Users/behri/OneDrive/Desktop/Master LSE/Essay/Ideas/Pepsi Coke/final_data.csv")
data_distance = pd.read_csv(r"C:/Users/behri/OneDrive/Desktop/Master LSE/Essay/Ideas/Pepsi Coke/distance_data.csv")

### INSTRUMENT VARIABLES ###

# Assign weeks 

week = 146
for i, idx in enumerate(data_gasoline.index): 
    data_gasoline.loc[idx, "WEEK"] = week + i

## Calculate the total cost for each shipment (in total gas payed), I do so by using: 
## Total_Expenditure = (Price / Gallon) * (Gallon / mile) * mile
## I use a constant fuel consumption of 1 / 6.5 gallons/mile and use the distance calculated before for the milage 

fuel_consumption = np.divide(1 , 6.5) ## (6.5 miles / gallon)

data_distance = data_distance[["store", "Distance"]]
data_gasoline = data_gasoline[["GASREGW", "WEEK"]]

data_distance["key"] = 1
data_gasoline["key"] = 1

instrument_data = pd.merge(data_distance, data_gasoline, on = "key").drop("key", axis = 1)

instrument_data["total_expenditure"] = instrument_data["Distance"] * instrument_data["GASREGW"] * fuel_consumption

# This instrument varies at the week-store level, we need it to vary at the product-week-store level in order to obtain a distinct instrument. 

# In order for the instrument to vary at the product scale, I first interact the instrument with the variable "Liquid_ml", this introduces some variation across products
instrument_merge = instrument_data.merge(data, how = "inner", left_on = ["store", "WEEK"], right_on = ["STORE", "WEEK"])[["UPC", "STORE", "WEEK", "PRICE", "DESCRIP", "BRAND", "COMPANY", "Liquid_ml", "PACKAGING", "nest", "Distance", "total_expenditure"]]
instrument_merge = instrument_merge.sort_values(by = ["STORE"])

count = data.groupby(["WEEK", "STORE"]).size().rename("Count")
instrument_merge = instrument_merge.merge(count, how = "inner", on = ["WEEK", "STORE"]).iloc[:, :-1]

## This instrument still does not vary at the product scale -> idea: use an average of "move" over all timeperiods (eliminate time-effects to get variation at product-level)
## In order to get a variable that represents that a higher quantity of products would have to be imported weekly 

data_grouped = data.groupby(["STORE", "WEEK", "UPC"])[["STORE", "WEEK", "UPC", "total_liquid_sold"]].transform("mean")
data_grouped = data_grouped.rename(columns = {"total_liquid_sold": "avg_total_liq"})

instrument_merge = instrument_merge.merge(data_grouped, how = "inner", on = ["WEEK", "STORE", "UPC"])
instrument_merge["total_expenditure"] = instrument_merge["avg_total_liq"] * instrument_merge["total_expenditure"]

# This instrument now varies at the product level and can hence in the next stage be used in order to test validity using 2SLS etc. 

count_nests = data.groupby(["WEEK", "nest"]).size().rename("Count")


## BLP-Style instruments: Count of competing products / aggregate characteristics 

# This terminology is somewhat ambiguous and hence there are multiple layers of substitution to consider 

# Layer 1: BLP with own-firm products -> substitution across brand

instrument_merge["group_liquid_sum"] = instrument_merge.groupby(["WEEK", "STORE", "brand"])["Liquid_ml"].transform("sum")
instrument_merge["blp_liquid_sum"] = instrument_merge["group_liquid_sum"] - instrument_merge["Liquid_ml"]


        