import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor 
from sklearn.linear_model import LinearRegression, Lasso, LassoCV
from sklearn.metrics import mean_squared_error
from stargazer.stargazer import Stargazer

data = pd.read_csv(r"C:/Users/behri/OneDrive/Desktop/Master LSE/Essay/Ideas/Pepsi Coke/data_estimation.csv")

# I want to run some preliminary steps in order to determine the multicollinearity of my data and 
# and run a LASSO regression in order to identify any features that might be redundant 

# 1. Calculate VIF 

# My controls are: Brand Dummies, liquid_sold, diet_indicator, no_caffeine_indicator, flavour dummy, package dummy, 
# season dummy, age dummy, ethnic, educ, nocar, income, hsizeavg, d_j 

dummys = []
prefixes = ["BRAND_", "DUMMY_", "SEASON_", "PROMOTION", "PACKAGE"]

for col in data.columns: 
    if col.upper().startswith(tuple(prefixes)):
        dummys.append(col)

X = data[dummys + ["age60", "ethnic", "educ", "nocar", "income", "D_j", "hsizeavg", "age9", "PRICE_x", "Liquid_ml_x"]]
X = X.drop(columns = ["BRAND_x"], axis = 1)

# Create variance inflation factor 

vif_data = pd.DataFrame()
vif_data["feature"] = X.columns 

vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]

# There is *some* cause for concern for the variables income, hsizeavg and age9 
# -> I will drop them for robustness in my analysis later.

# 2. Performing feature selection (LASSO regression)
y = data["LHS"]

# Use Cross Validation in order to determine the optimal alpha 
lasso_cv = LassoCV(cv = 5, random_state = 42)
lasso_cv.fit(X,y)
optimal_alpha = lasso_cv.alpha_

lasso = Lasso(alpha = 0.1)
lasso.fit(X,y)

# Calculate predictions and MSE 
predictions = lasso.predict(X)
mse_lasso = mean_squared_error(y, predictions)

print("Lasso MSE:", mse_lasso)

# Create Df to display the results 
coefficients = pd.DataFrame({
    "Feature": X.columns,
    "Coefficient": lasso.coef_
    })

# Which coefficients get shrunk to zero? 
zero_coefficients = coefficients[coefficients["Coefficient"] == 0]

# Among others, LASSO also identifies these features as potentially problematic! I will hence later drop these for robustness analysis...




## ADD DESCRIPTIVE VARIABLES FOR THE MOST IMPORTANT VARIABLES IN THE ORIGINAL DATASET
descriptive_data = data[["PRICE_x", "MOVE", "Liquid_ml_x", "rev"]]
descriptive_data = descriptive_data.rename(columns = {"PRICE_x": "Price", "MOVE": "Total Quantity Sold", "rev": "Revenue Generated ($)", "Liquid_ml_x": "Amount of liquid per product"})
descriptive_data = descriptive_data.describe()

data_demographics = pd.read_stata(r"C:/Users/behri/OneDrive/Desktop/Master LSE/Essay/Ideas/Pepsi Coke/demo.dta")
data_demographics = data_demographics.dropna(how = "all", axis = 1)
data_demographics = data_demographics[["age60", "educ", "income"]]
data_demographics = data_demographics.dropna(how = "all", axis = 0)
data_demographics = data_demographics.rename(columns = {"age60": "% of > 60 year-olds", "educ": "% of college graduates", "income": "median log income"})
descriptive_demo = data_demographics.describe()

description = descriptive_data.join(descriptive_demo)
for col in description.columns:
    description[col] = description[col].astype(int)
    
description = description.T


    
latex_description = description.to_latex(
    float_format = "%.2f",
    caption = "Summary Statistics",
    label = "tab:summary_stats",
    column_format = "lcccccccc",
    position = "htpb"
)

print(latex_description) 


