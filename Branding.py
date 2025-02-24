# BRAND ASSIGNING 
import pandas as pd 
import numpy as np 
import re
import datetime as dt 

#Function to assign brands: 
def assign_grouped_brand(desc):
    """
    Given a product description, return a grouped brand name.
    For example, if the description mentions any variation of Coke 
    (e.g., "Coke", "Cherry Coke", "Coca Cola", etc.), the function 
    returns "Coke".
    """
    d = desc.upper()
    # Each tuple consists of: (grouped brand, list of keywords that indicate that group)
    brand_groups = [
        ("Pepsi", ["CRYSTAL PEPSI", "PEPSI"]),
        ("Mountain Dew", ["MOUNTAIN DEW", "MTN DEW"]),
        ("Mug", ["MUG"]),
        ("Slice", ["SLICE"]), 
        ("Lipton", ["LIPTON BRISK"]),
        ("Coke",  ["COKE II", "CHERRY COKE", "COCA COLA", "COKE", "CAFF FREE CLASSIC CO"]),
        ("Sprite", ["SPRITE"]),
        ("Barq", ["BARQ"]), 
        ("Tab", ["TAB"]),
        ("Minute Maid", ["MINUTE MAID"]),
        ("Enduro", ["ENDURO"]),
        ("Dr Pepper", ["DR. PEPPER", "DR PEPPER"]),
        ("7 Up", ["7-UP", "7UP", "CHERRY 7 UP"]),
        ("RC Cola", ["ROYAL CROWN", "R.C.", "RC ", "DIET RITE", "NEHI"]),
        ("A&W", ["A&W"]),
        ("Sunkist", ["SUNKIST"]),
        ("Crush", ["CRUSH"]),
        ("Squirt", ["SQUIRT"]),
        ("Canada Dry", ["CAN DRY"]),
        ("Schweppes", ["SCHWEPPES"]),
        ("Canfield", ["CANFIELD"]),
        ("Tetley", ["TETELY", "TETLEY"]),
        ("Old Towne", ["OLD TOWNE", "OLD TOWN"]),
        ("Orenzada",      ["ORENZADA"]),         
        ("Lemoniada",     ["LEMONIADA"]),
        ("Seltzer",       ["WODA SODOWA", "SELTZER"]),
        ("Mandarynada",   ["MANDARYNDA"]),
        ("Dad's Root Beer", ["DADS ROOT BEER", "DAD'S ROOT BEER"]),
        ("Hawaiian Punch",  ["HAWAIIAN PUNCH"]),
        ("Dominick's",      ["DOMINICK'S"]),
        ("S&W",             ["S&W"]),
        ("Upper 10",        ["UPPER 10"]),
        ("WLWD",            ["WLWD"]),
        ("Big Red",         ["BIG RED"]),
        ("Seagram's Ginger Ale", ["SEAGRAM'S GINGER ALE"]),
        ("Ocean Spray",     ["OCEAN SPRAY"]),
        ("Sunny Delight",   ["SUNNY DELIGHT"]),
        ("Country Time",  ["COUNTRYTIME"]),
        ("Welch's",       ["WELCH'S"]),
    ]
    
    
    # Loop over the groups and return the first matching brand.
    for brand, keywords in brand_groups:
        for kw in keywords:
            if kw in d:
                return brand
    return "Other"


def assign_company(desc):
    """
    Given a product description, determine the grouped brand and then 
    return the historical parent company (1988–1996) that owned that brand.
    """
    brand = assign_grouped_brand(desc)
    
    # Mapping from grouped brand to historic parent company.
    company_mapping = {
        "Pepsi": "PepsiCo",
        "Mountain Dew": "PepsiCo",
        "Mug": "PepsiCo",
        "Slice": "PepsiCo", 
        "Lipton": "PepsiCo",
        "Coke": "Coca-Cola",
        "Sprite": "Coca-Cola",
        "Barq": "Coca-Cola",
        "Tab": "Coca-Cola",
        "Minute Maid": "Coca-Cola",
        "Enduro": "Enduro",
        "Dr Pepper": "Dr Pepper Inc.",
        "7 Up": "7 Up Inc.",
        "RC Cola": "RC Cola",
        "A&W": "A&W",
        "Sunkist": "Sunkist Growers",
        "Crush": "Cadbury Schweppes",
        "Squirt": "7 Up Inc.",
        "Canada Dry": "Cadbury Schweppes",
        "Schweppes": "Cadbury Schweppes",
        "Canfield": "Canfield",
        "Tetley": "Tetley",
        "Old Towne": "Old Towne",
        "Country Time": "Kraft",
        "Welch's": "Welch's",
        "Orenzada": "Other",
        "Lemoniada": "Other",
        "Seltzer": "Other",
        "Mandarynada": "Other",
        "Dad's Root Beer": "Dad's Root Beer Co.",
        "Hawaiian Punch": "Nestlé",
        "Dominick's": "Dominick's",
        "S&W": "S&W",
        "Upper 10": "RC Cola",
        "WLWD": "Other",
        "Big Red": "Big Red Inc.",
        "Seagram's Ginger Ale": "Seagram's",
        "Ocean Spray": "Ocean Spray",
        "Sunny Delight": "Sunny Delight"
    }
    
    return company_mapping.get(brand, "Other")
    
data = pd.read_csv(r"C:/Users/behri/OneDrive/Desktop/Master LSE/Essay/Ideas/Pepsi Coke/cleaned_data.csv")

data["BRAND"] = data["DESCRIP"].apply(assign_grouped_brand)
data["COMPANY"] = data["DESCRIP"].apply(assign_company)

# Diet / Non-Diet 

def diet_indicator(desc): 
    d = desc.upper()
    if "DIET" in d: 
        return 1
    else:
        return 0 
    
def no_caffeine_indicator(desc) :
    d = desc.upper()
    if ("CAFF." in d or "CAFF FREE" in d or "CAFF-FREE" in d or "CAFFEINE FREE" in d) : 
        return 1 
    else: 
        return 0

data["Diet_Indicator"] = data["DESCRIP"].apply(diet_indicator)
data["No_Caffeine_Indicator"] = data["DESCRIP"].apply(no_caffeine_indicator)

#Create dummy variables for taste 
def assign_flavour_category(description: str) -> str:
    desc = description.upper()

    # --- 1) Cola ---
    if any(word in desc for word in [
        "COLA", "COKE", "PEPSI", "RC COLA", "DR PEPPER", "DR. PEPPER",
        "R.C.", "TAB", "CRYSTAL PEPSI"
    ]):
        return "Cola"

    # --- 2) Orange ---
    if any(word in desc for word in [
        "ORANGE", "SUNKIST", "MANDARYNDA", "CRUSH"
    ]):
        return "Orange"

    # --- 3) Lemon/Citrus-Based ---
    if any(word in desc for word in [
        "MOUNTAIN DEW", "SPRITE", "7-UP", "SQUIRT", "UPPER 10",
        "LEMONADE", "LEMON-LIME", "LEM-LIME", "ICED TEA", "BRISK", "TEA"
    ]):
        return "Lemon/Citrus-Based"

    # --- 4) Mixed Fruit ---
    if any(word in desc for word in [
        "CHERRY", "GRAPE", "BERRY", "STRAWBERRY", "STRAW", "WELCH",
        "PINEAPPLE", "TROPICAL", "POLYNESIAN", "PUNCH", "MANGO", "BANANA",
        "PEACH"
    ]):
        return "Mixed Fruit"

    # --- 5) Other ---
    return "Other"

data["Flavour"] = data["DESCRIP"].apply(assign_flavour_category)
dummy_vars = pd.get_dummies(data["Flavour"], prefix = "Flavour")
dummy_vars = dummy_vars.drop(columns = ["Flavour_Other"])
data = pd.concat([data, dummy_vars], axis = 1)
#data = data.drop(columns = ["Flavour"])


#Create more precise variable that indicates the "amount of liquid" that is being bought
OZ_TO_ML = 29.5735

def convert_to_milliliters(size):
    # Standardize and trim
    size = size.upper().strip()

    # 1) Multi-pack pattern: e.g. "6/12OZ", "8/16OZ", "24/12O" (assuming the missing 'Z' still means oz)
    #    This will capture something like "6/20 O" as 6 * 20 oz
    match = re.match(r"^(\d+)\s*/\s*(\d+(?:\.\d+)?)\s*(?:OZ|O)\b", size)
    if match:
        num_units = float(match.group(1))
        oz_per_unit = float(match.group(2))
        return num_units * oz_per_unit * OZ_TO_ML

    # 2) Single measurement in Ounces (with optional decimal): e.g. "16 OZ", "7.5 OZ", "20 OZ", "7.5 O"
    match = re.match(r"^(\d+(?:\.\d+)?)\s*(?:OZ|O)\b", size)
    if match:
        return float(match.group(1)) * OZ_TO_ML

    # 3) Single measurement in Liters (with optional decimal): e.g. "1 LT", "2 L", "3.5 LT"
    match = re.match(r"^(\d+(?:\.\d+)?)\s*(?:L|LT)\b", size)
    if match:
        return float(match.group(1)) * 1000

    # 4) Single measurement in mL (with optional decimal): e.g. "500 ML", "750 ML", "1000 ML"
    match = re.match(r"^(\d+(?:\.\d+)?)\s*ML\b", size)
    if match:
        return float(match.group(1))

    #5) Handle 24EA etc.
    if size in ["24 EA", "24 PK", "24 PAC"]:
        return 24*355
    
    return None

def final_amount(data): 
    data["Liquid_ml"] = data["SIZE"].apply(convert_to_milliliters)
    if "QTY" in data.columns: 
        data["Liquid_ml"] = data["Liquid_ml"] * data["QTY"]
    else: 
        pass 
    return data 

data = final_amount(data)

## Refine average price ##
#Clear certain missing average prices
data["AVG_PRICE"] = data.groupby(["WEEK", "BRAND"])["PRICE"].transform("mean")
data["AVG_PRICE_WEEK"] = data["AVG_PRICE"]
data = data.drop(columns=["AVG_PRICE"])

def assign_biggest_brands(avg_price):
    if avg_price >= 4: 
        return avg_price
    else: 
        return None 

def assign_packaging_type(size, descrip):
    d = str(descrip).upper()
    size_upper = size.upper().strip()
    single_serve_bottles = {"EACH", "1 LT", "7.5 OZ", "16 OZ", "20 OZ"}
    
    if "CANS" in d: 
        return "Cans"
    
    if size_upper in ("2 LT", "3 LT"): 
        return "Larger Bottles"
    
    if size_upper in single_serve_bottles: 
        return "Single-Serve Bottles"
    
    return "Multi-Packs"
    

data["AVG_PRICE_WEEK"] = data["AVG_PRICE_WEEK"].apply(assign_biggest_brands)

data["PACKAGING"] = data.apply(lambda row: assign_packaging_type(row["SIZE"], row["DESCRIP"]), axis = 1)

dummy_packaging = pd.get_dummies(data["PACKAGING"], prefix = "Package")
dummy_packaging = dummy_packaging.drop(columns = ["Package_Single-Serve Bottles"])

data = pd.concat([data, dummy_packaging], axis = 1)

## Add promotion dummy 

data["Promotion"] = data["SALE"].notna().astype(int)

## Add quarters 
start_date = pd.to_datetime("1989-09-14")
end_date = pd.to_datetime("1989-09-20")
data["date"] = start_date + pd.to_timedelta((data["WEEK"] - 1) * 7, unit= "d")
data["date_end"] = end_date + pd.to_timedelta((data["WEEK"] - 1) * 7, unit = "d")
data["quarter"] = pd.PeriodIndex(data.date, freq = "Q")
data["quarter_str"] = data["quarter"].astype(str)

data["date_str"] = data["date"].astype(str)
data["date_end_str"] =data["date_end"].astype(str)

## Add seasons 
data["quarter_number"] = data["quarter_str"].str.split("Q").str[1]
season_mapping = {
    "1": "Winter", 
    "2": "Spring", 
    "3": "Summer", 
    "4": "Autumn" 
}

data["season"] = data["quarter_number"].map(season_mapping)

### CREATE HOLIDAY DUMMY ###

# Cache to store holidays for a given year
holiday_cache = {}

def get_holidays(year):
    if year in holiday_cache:
        return holiday_cache[year]
    
    holidays = {
        "Christmas": pd.Timestamp(year, 12, 25),
        "Halloween": pd.Timestamp(year, 10, 31),
        "4th of July": pd.Timestamp(year, 7, 4),
        "New Years Eve": pd.Timestamp(year, 12, 31)
    }
    
    # President's Day (Third Monday in February)
    feb_first = pd.Timestamp(year, 2, 1)
    # Calculate offset to first Monday in February:
    offset = (7 - feb_first.weekday()) % 7
    first_monday_feb = feb_first + pd.Timedelta(days=offset)
    # Third Monday is two weeks after the first Monday:
    holidays["Presidents Day"] = first_monday_feb + pd.Timedelta(days=14)
    
    # Labour Day (First Monday in September)
    sep_first = pd.Timestamp(year, 9, 1)
    offset = (7 - sep_first.weekday()) % 7
    holidays["Labour Day"] = sep_first + pd.Timedelta(days=offset)
    
    # Memorial Day (Last Monday in May)
    may_last = pd.Timestamp(year, 5, 31)
    # If may_last is not Monday, subtract the necessary days
    offset = may_last.weekday()  # Monday is 0; if not, this gives the number of days to subtract.
    holidays["Memorial Day"] = may_last - pd.Timedelta(days=offset)
    
    
    # Thanksgiving (Fourth thursday in November)
    nov_first = pd.Timestamp(year, 11, 1)
    offset = (10  - nov_first.weekday()) % 7
    fourth_thursday_nov = nov_first + pd.Timedelta(days = 21 + offset)
    holidays["Thanksgiving"] = fourth_thursday_nov
    
    easter_dates = {
     1989: (3, 26),
     1990: (4, 15),
     1991: (3, 31),
     1992: (4, 19),
     1993: (4, 11),
     1994: (4, 3),
     1995: (4, 16),
     1996: (4, 7),
    }
    
    if year in easter_dates: 
        m, d = easter_dates[year]
        holidays["Easter"] = pd.Timestamp(year, m, d)
        
    # Cache the computed holidays for this year
    holiday_cache[year] = holidays
    return holidays

def assign_holiday(date, date_end):
    start = pd.to_datetime(date)
    end = pd.to_datetime(date_end)
    
    # Assume the holiday's year is the same as the start of the week.
    year = start.year
    
    # Retrieve the holidays for the given year (using caching)
    holidays = get_holidays(year)
    
    # Check if any holiday falls within the week
    holidays_in_week = [name for name, hol_date in holidays.items() if start <= hol_date <= end]
    
    return ", ".join(holidays_in_week) if holidays_in_week else "No Holiday"

data["holiday"] = data.apply(lambda x: assign_holiday(x["date"], x["date_end"]), axis=1)

def is_holiday(holiday):
    if holiday == "No Holiday":
        return 0 
    return 1 

data["holiday_indicator"] = data["holiday"].apply(is_holiday)
unique_holiday_data = data[["holiday", "date"]].drop_duplicates()

#Drop old columns

data = data.drop(columns = ['PRICE_HEX', 'PROFIT_HEX', 'COM_CODE','Unnamed: 0.1', 'Unnamed: 0'])

##Add further control variables
data_demographics = pd.read_stata(r"C:/Users/behri/OneDrive/Desktop/Master LSE/Essay/Ideas/Pepsi Coke/demo.dta")

data_demographics = data_demographics[data_demographics["mmid"].isna() == False]

data_demographics_for_merge = data_demographics[["store", "age9", "age60", "ethnic", "educ", "nocar", "income", "hsizeavg"]]
data = pd.merge(
    data,
    data_demographics_for_merge,
    how = "left", 
    left_on = "STORE", 
    right_on = "store"
)

def impute_mean(col):
     mean_val = np.mean(col)
     return col.fillna(mean_val)

columns_to_impute = ("age9", "age60", "ethnic", "educ", "nocar", "income", "hsizeavg")

for col in columns_to_impute:
    data[col] = impute_mean(data[col])


## Remove Blood Glucose Screen (key: UPC = 179)
data = data[data["UPC"] != 179]

## Find the first month where there is more than just one brand (Pepsi)
data_more_than_one_brand = data[(data["COMPANY"] != "PepsiCo")]
data_more_than_one_brand = data_more_than_one_brand.sort_values(["WEEK"])
data = data[data["WEEK"] >= 147]
## Remove smaller brands (following Allender and Richards (2012) approach)

# Identify the sum of sales of all brands and take 40 biggest brands
data_sum_brands = data.groupby(by = ["UPC", "DESCRIP"], axis = 0)["MOVE"].sum()
data_sum_brands = data_sum_brands.sort_values(ascending = False)
data_sum_brands = data_sum_brands.iloc[0:39]

# Merge to old dataframe (inner)
data = data.merge(data_sum_brands, how = "inner", on = ["UPC", "DESCRIP"]) 
data = data.rename(columns = {"MOVE_y": "SUM_MOVE", "MOVE_x": "MOVE"})
data = data.sort_values(["WEEK"])


## Add outside option - Definition as given by Mariuzzo (2003) - Determine the maximum daily consumption per person per day in Chicago and "relative market size" is 330ml per day 
data["total_liquid_sold"] = data["MOVE"] * data["Liquid_ml"]
data_consumption = data.groupby(["WEEK"])[["total_liquid_sold", "MOVE"]].sum()

#Because our model assumes that we only buy one "option" per customer, we can calculate the number of liquid consumed by those who came in the store per day per person
data_demographics["household_mean"] = np.mean(data_demographics["hsizeavg"])
data_consumption["daily_consumption"] = data_consumption["total_liquid_sold"] / (data_consumption["MOVE"] * 7 * data_demographics["hsizeavg"].mean())

# Define potential market size as 500ml a day per person 
avg_serving_size = (data["Liquid_ml"].mean()) / 7
data_consumption["outside_move"] = (550 - data_consumption["daily_consumption"]) / avg_serving_size
data_consumption["total_moves"] = data_consumption["MOVE"] + data_consumption["outside_move"]
total_moves = data_consumption["total_moves"]

# Calculate the market share as Move_i / Total_Move where Total_Move = Number of observed moves + outside_moves -> hypothetical market size of 500 ml consumption per person per day 
data = data.merge(total_moves, on = "WEEK", how = "left")
data["market_share"] = data["MOVE"] / data["total_moves"]

#data.to_csv(r"C:/Users/behri/OneDrive/Desktop/Master LSE/Essay/Ideas/Pepsi Coke/final_data.csv")
