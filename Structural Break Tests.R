rm(list = ls())
library(tidyverse)
library(haven)
library(dplyr)

install.packages("desk", lib = "C:/Program Files/RStudio/locales")

data <- read.csv("C:/Users/behri/OneDrive/Desktop/Master LSE/Essay/Ideas/Pepsi Coke/final_data.csv")

# Create sub-dataframe only for Pepsi and Coke Products 

data_pepsi <- data %>%
  filter(COMPANY == "PepsiCo")

#Estimate QLR test

# Assume the model is: ln(price) = promotion_it + week_t + epsilon_it 

price.est_pepsi <- lm(log(PRICE) ~ Promotion + WEEK, data = data_pepsi)

my.qlr <- qlr.test(price.est, from = 290, to = 350, details = TRUE)
print(my.qlr)
plot(my.qlr)
