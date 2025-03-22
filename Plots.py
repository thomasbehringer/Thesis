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

data_group_quarter = data.groupby(by = ["quarter"])["STORE"].nunique()

# Plot this dataset to get an intuition for the degree of "missingness" of stores
plt.figure(figsize = (12,6))
plt.plot(data_group_quarter.index, data_group_quarter.values)
plt.title("Number of Stores in each quarter of the dataset")
plt.xlabel("Quarter")
plt.ylabel("Number of Stores")
plt.xticks(rotation = 45)
plt.legend()
plt.show()

# The dataset seems to be fairly well - balanced -> there is almost no endogenous exit (there are also data quality issues to consider!) 

# Q: Does the dataset exhibit MAR/MCAR/MNAR? 

# A: To test missingness, we need to use an indicator for missingness 

# Use Little's MCAR test in order to test for the possibility of the data missing completely at random -> no endogenous reason for missingness! 



## ANALYSE THE DISTRIBUTION OF THE HIGHEST COMPANIES 

# Q: How are the sales in the dataset distributed - Which firms are the biggest? 

# A: We need to look at different statistics that give rise to some index of how well-distributed sales are 

# Metric : Gini-Coefficient (give reasoning in the paper)

# In order to do this, I will consider different metrics...

# 1. Take the number of sales for each company 
data_group_company_sales = data.groupby(by = ["COMPANY"])["MOVE"].sum()
data_group_company_sales = data_group_company_sales.sort_values(ascending = True)

sum_values = int(data_group_company_sales.sum())
data_group_company_sales_pct = data_group_company_sales / sum_values

cumulative_sales = data_group_company_sales_pct.cumsum()

# 2. Take the total revenue of each firm
data_group_company_rev = data.groupby(by = ["COMPANY"])["rev"].sum()
data_group_company_rev = data_group_company_rev.sort_values(ascending = True)

sum_values = int(data_group_company_rev.sum())
data_group_company_rev_pct = data_group_company_rev / sum_values 

cumulative_rev = data_group_company_rev_pct.cumsum()

total_firms = len(cumulative_sales.index)

data_plot = pd.DataFrame(data = [data_group_company_sales, data_group_company_rev]).T
data_plot = data_plot.reset_index()

data_plot["Number"] = range(1, len(data_plot) + 1)
data_plot["Number"] = data_plot["Number"] / sum(data_plot["Number"]) 
data_plot["Number"] = data_plot["Number"].cumsum()
 
plt.figure(figsize = (12,6))
plt.plot(data_plot["Number"], cumulative_sales.values, label = "No. of sales", color = "red")
plt.plot(data_plot["Number"], cumulative_rev.values, label = "Total revenue", color = "blue")
plt.plot([0,1], [0,1], color = "black", linestyle = "--")
plt.title("Lorenz Curve for firms")
plt.xlabel("Cumulative Share of Firms")
plt.ylabel("Cumulative Share of Market")
plt.xticks(rotation = 45)
plt.legend()
plt.show()

# Calculating gini-coefficients: 
def gini_coefficient(x): 
    x = np.sort(np.array(x))
    n = len(x)
    index = np.arange(1, n+1)
    
    return (2 * np.sum(index * x) / (n * np.sum(x)) - (n+1) / n)

sales_values = data_group_company_sales.values 
revenue_values = data_group_company_rev.values
gini_sales = gini_coefficient(sales_values)
gini_revenue = gini_coefficient(revenue_values)
print("Gini coefficient for sales:", gini_sales)
print("Gini coefficient for revenue:", gini_revenue)


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