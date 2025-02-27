import numpy as np 
import pandas as pd 

data_gasoline = pd.read_csv(r"C:/Users/behri/OneDrive/Desktop/Master LSE/Essay/Ideas/Pepsi Coke/GASREGW.csv")
data = pd.read_csv(r"C:/Users/behri/OneDrive/Desktop/Master LSE/Essay/Ideas/Pepsi Coke/final_data.csv")
data_distance = pd.read_csv(r"C:/Users/behri/OneDrive/Desktop/Master LSE/Essay/Ideas/Pepsi Coke/distance_data.csv")

## INSTRUMENT VARIABLES ## 

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
