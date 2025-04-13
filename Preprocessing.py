import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor 
from sklearn.linear_model import LinearRegression, Lasso, LassoCV
from sklearn.metrics import mean_squared_error
#from stargazer.stargazer import Stargazer
import matplotlib.pyplot as plt

data = pd.read_csv(r"C:/Users/behri/OneDrive/Desktop/Master LSE/Essay/Ideas/Pepsi Coke/data_estimation.csv")

# I want to run some preliminary steps in order to determine the multicollinearity of my data and 
# and run a LASSO regression in order to identify any features that might be redundant 

# 1. Calculate VIF 

# My controls are: Brand Dummies, liquid_sold, diet_indicator, no_caffeine_indicator, flavour dummy, package dummy, 
# season dummy, age dummy, ethnic, educ, nocar, income, hsizeavg, d_j 


X = data[['Diet_Indicator',
       'No_Caffeine_Indicator', 'Flavour_Cola', 'Flavour_Lemon/Citrus-Based',
       'Flavour_Mixed Fruit', 'Flavour_Orange', 'Liquid_ml_x', 'Package_Cans',
       'Package_Larger Bottles', 'Package_Multi-Packs']]

# Create variance inflation factor (VIF) dataframe for diagnostic purposes.
from statsmodels.stats.outliers_influence import variance_inflation_factor

vif_data = pd.DataFrame()
vif_data["feature"] = X.columns 
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]
print(vif_data)

# Define target variable.
y = data["LHS"]

# Optional: Run LassoCV to get the optimal alpha (for reference)
from sklearn.linear_model import LassoCV

lasso_cv = LassoCV(cv=5, random_state=42)
lasso_cv.fit(X, y)
optimal_alpha = lasso_cv.alpha_
print("Optimal alpha from CV:", optimal_alpha)

# Now, we run Lasso over a range of lambda values on a logarithmic scale.
# Generate 100 lambda (alpha) values between 10^-4 and 10^4.
alphas = np.logspace(-4, 4, 100)

# Create an empty array to store coefficients for each lambda.
# The array shape is (number of alphas, number of features)
coefs = np.zeros((len(alphas), X.shape[1]))

# Loop through each alpha value, perform Lasso, and store the coefficients.
for i, alpha in enumerate(alphas):
    # Increase max_iter if needed for convergence.
    lasso = Lasso(alpha=alpha, max_iter=10000, random_state=42)
    lasso.fit(X, y)
    coefs[i, :] = lasso.coef_

# Plot the coefficient paths.
plt.figure(figsize=(10, 6))
for j, col in enumerate(X.columns):
    plt.plot(alphas, coefs[:, j], label=col)
plt.xscale("log")
plt.xlabel("Lambda (alpha)")
plt.ylabel("Coefficient value")
plt.title("Lasso Coefficient Paths")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

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


