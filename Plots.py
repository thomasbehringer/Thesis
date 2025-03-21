import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv(r"C:/Users/behri/OneDrive/Desktop/Master LSE/Essay/Ideas/Pepsi Coke/final_data.csv")
data_final = pd.read_csv(r"C:/Users/behri/OneDrive/Desktop/Master LSE/Essay/Ideas/Pepsi Coke/data_estimation.csv")
data_raw = pd.read_csv(r"C:/Users/behri/OneDrive/Desktop/Master LSE/Essay/Ideas/Pepsi Coke/joined_data.csv")

## ANALYSE QUALITY OF THE DATASET ## 

# Q: Is the dataset balanced? 

# A: We need to look at the number of firms in each quarter/week? If the number of stores drastically declines/changes 
# -> evidence for unbalanced dataset

data_group_quarter = data.groupby(by = ["quarter"])["STORE"].count() 

# Plot this dataset to get an intuition for the degree of "missingness" of stores
plt.figure(figsize = (12,6))
plt.plot(data_group_quarter.index, data_group_quarter.values)
plt.title("Number of Firms in each week of the dataset")
plt.xlabel("Quarter")
plt.ylabel("Number of Firms")
plt.xticks(rotation = 45)
plt.legend()
plt.show()

# The dataset seems to start off with a low number of stores but then hits a peak and stays at that level 

# There seems to be some issues with endogenous entry in this dataset but I will not model this (talk about paper that talks about inconsistencies due to unbalanced dataset -> take data as is)

## ANALYSE THE DISTRIBUTION OF THE HIGHEST COMPANIES 

# Q: How are the sales in the dataset distributed - Which firms are the biggest? 

# A: We need to look at different statistics that give rise to some index of how well-distributed sales are 

# Metric : Gini-Coefficient (give reasoning in the paper)

# In order to do this, I will consider different metrics...

# 1. Simply take the number of all observations grouped by the company

data_group_company = data.groupby(by = ["COMPANY"])["QTY"].sum()
data_group_company = data_group_company.sort_values(ascending = True)

sum_values = int(data_group_company.sum())
data_group_company_pct = data_group_company / sum_values

cumulative = data_group_company_pct.cumsum()

plt.figure(figsize = (12,6))
plt.plot(cumulative.index, cumulative.values, label = "No. of products")
plt.axline([0,0], [10,1])
plt.title("Lorenz Curve for firms")
plt.xlabel("Firm")
plt.ylabel("Percentage of entire market")
plt.xticks(rotation = 45)
plt.legend()
plt.show()

# Plot average quarterly prices
    
data["AVG_price_quarter"] = (data.groupby(["COMPANY", "quarter"]))["PRICE"].transform("mean")

data_prices = data.pivot_table(
    index = "quarter",
    columns = "COMPANY", 
    values = "AVG_price_quarter",
    aggfunc = "mean").sort_index()

for brand in ["PepsiCo", "Coca-Cola"]:
    plt.plot(data_prices.index, data_prices[brand], label=brand)

plt.title("Average Prices of PepsiCo and Coca-Cola Over Time")
plt.xlabel("Quarters")
plt.ylabel("Average Prices")
plt.xticks(rotation=45)
plt.legend()  # Add legend to differentiate brands
plt.show()