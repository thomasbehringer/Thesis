import pandas as pd
import numpy as np

data = pd.read_csv(r"C:/Users/behri/OneDrive/Desktop/Master LSE/Essay/Ideas/Pepsi Coke/final_data.csv")

## Further transform the data according to the procedure in Mariuzzo and Walsh (2003):

## Find a way to model the consumer's transportation costs

# Find weights for each store 

total_sales = data.groupby("WEEK")["MOVE"].sum().reset_index(name = "total_move")
store_week_sales = data.groupby(["WEEK", "STORE"])["MOVE"].sum().reset_index(name = "store_move")

store_week_sales = store_week_sales.merge(total_sales, on = "WEEK")
store_week_sales["store_weight"] = store_week_sales["store_move"]/store_week_sales["total_move"]

#Drop duplicates if there are more than one entry for a given (store, week, product) combination
store_products = data[["STORE", "WEEK", "NITEM"]].drop_duplicates()

store_products = store_products.merge(
    store_week_sales[["STORE", "WEEK", "store_weight"]],
    on = ["WEEK", "STORE"],
    how = "left"
)

effective_coverage = store_products.groupby(["WEEK", "NITEM"])["store_weight"].sum().reset_index(name = "effective_coverage")

#Calculate distance for each product: 
effective_coverage["D_j"] = 1 - effective_coverage["effective_coverage"]

# Merge on original data 
data = data.merge(effective_coverage[["WEEK", "NITEM", "effective_coverage", "D_j"]], 
                  on = ["WEEK", "NITEM"], 
                  how = "left")

# CALCULATE THE OUTSIDE GOOD 

# IDEA: LOOK AT HIGHEST NUMBER OF "Liquid" Sold per person per day in Chicago and estimate some additional sales