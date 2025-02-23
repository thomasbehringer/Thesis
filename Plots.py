import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_csv(r"C:/Users/behri/OneDrive/Desktop/Master LSE/Essay/Ideas/Pepsi Coke/final_data.csv")

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