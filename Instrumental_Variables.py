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
instrument_merge = instrument_data.merge(data, how = "inner", left_on = ["store", "WEEK"], right_on = ["STORE", "WEEK"])[["UPC", "STORE", "WEEK", "PRICE", "DESCRIP", "BRAND", "COMPANY", "Liquid_ml", "PACKAGING", "Distance", "total_expenditure", "nest", "hyp_market"]]
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

# Within each layer, we can choose for example the mean of the liquid_ml which does not include the product itself or the number of other products by the same brand in the market 

# First, compute the overall sum and count of Liquid_ml for each store-week group
group_sum = instrument_merge.groupby(['WEEK', 'STORE'])['Liquid_ml'].transform('sum')
group_count = instrument_merge.groupby(['WEEK', 'STORE'])['Liquid_ml'].transform('count')

# Next, compute the sum and count of Liquid_ml for the current product's own brand within each store-week
own_brand_sum = instrument_merge.groupby(['WEEK', 'STORE', 'BRAND'])['Liquid_ml'].transform('sum')
own_brand_count = instrument_merge.groupby(['WEEK', 'STORE', 'BRAND'])['Liquid_ml'].transform('count')

# Now, for each observation, the total of rival products equals the overall sum minus the sum for its own brand,
# and the count of rival products equals the overall count minus the count for its own brand.
rival_sum = group_sum - own_brand_sum
rival_count = group_count - own_brand_count

# Calculate the rival average Liquid_ml, handling cases where there are no rival products
instrument_merge['rival_liquid_avg'] = np.where(rival_count > 0, rival_sum / rival_count, np.nan)
instrument_merge['rival_total_count'] = rival_count

instrument_problem = instrument_merge[instrument_merge["rival_total_count"] == 0]

# There are some problematic columns, since they are very limited (18 rows), I will drop them.
instrument_merge = instrument_merge.dropna()
instrument_problem = instrument_merge[instrument_merge["rival_total_count"] == 0]

# I can now calculate the average Liquid_ml and the total count in the same market 
# and the same nest as well as the rival nest 

# I first calculate the number and average in the same market of a different nest 

# Calculate the total sum and count of Liquid_ml for each store-week-nest group
nest_group_sum = instrument_merge.groupby(['WEEK', 'STORE', 'nest'])['Liquid_ml'].transform('sum')
nest_group_count = instrument_merge.groupby(['WEEK', 'STORE', 'nest'])['Liquid_ml'].transform('count')

# For each observation, compute the rival nest sum and count by excluding its own product
instrument_merge['nest_avg'] = np.where(
    nest_group_count > 1,
    (nest_group_sum - instrument_merge['Liquid_ml']) / (nest_group_count - 1),
    np.nan  # use NaN if there is no rival product (i.e. group count = 1)
)

instrument_merge['nest_count'] = np.where(
    nest_group_count > 1,
    nest_group_count - 1,
    np.nan
)

test = instrument_merge.isna().sum()
# There are 187 missing rows now, I'll have to drop them again 
instrument_merge = instrument_merge.dropna()


# I can now calculate the number and average for the rival nest

instrument_merge['other_nest'] = instrument_merge['nest'].apply(lambda x: 'Other' if x == 'Cola' else 'Cola')

nest_week_stats = instrument_merge.groupby(['WEEK', 'nest']).agg(
    nest_count=('Liquid_ml', 'count'),
    nest_avg=('Liquid_ml', 'mean')
).reset_index()


nest_week_stats = nest_week_stats.rename(columns={
    'nest': 'other_nest',
    'nest_count': 'other_nest_count',
    'nest_avg': 'other_nest_avg'
})

# Merge the stats back to the original DataFrame on WEEK and the computed other_nest column
instrument_merge = instrument_merge.merge(nest_week_stats, on=['WEEK', 'other_nest'], how='left')

# I now have 6 + 1 = 7 Instruments - I will reconsider later about more instruments 

## MERGE DATASETS 

# I will now merge the two datasets in order to then have a final dataset which I can use to do my demand estimation and merger simulation 
data_final = data.merge(instrument_merge, how = "inner", on = ["UPC", "STORE", "WEEK"])

# I will select only the relevant columns...
data_final = data_final.drop(["Unnamed: 0", "SALE", "PROFIT", "OK", "SIZE", "CASE", "NITEM", "Flavour", 
                              "AVG_PRICE_WEEK", "PACKAGING_x", "date", "date_end", "quarter", "quarter_str", "date_str",
                              "date_end_str", "store", "effective_coverage", "nest_y", "PRICE_y", "DESCRIP_y", "BRAND_y", 
                              "COMPANY_y", "Liquid_ml_y", "PACKAGING_y"], axis = 1)

## Determine summary statistics of the Gasoline Price 
description = data_gasoline["GASREGW"].describe()
#data_final.to_csv(r"C:/Users/behri/OneDrive/Desktop/Master LSE/Essay/Ideas/Pepsi Coke/data_estimation.csv")