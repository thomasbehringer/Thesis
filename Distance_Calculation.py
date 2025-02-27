import pandas as pd 
import csv 
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

## This script attempts to recover the geodesic distance of each store to a specific bottling plant in South Chicago 
## in order to later use this information as an instrument for the price of the bottles 

## FIRST STEP: EXTRACT THE LONGITUDE AND LATTITUDE OF EACH STORE 

data_demographics = pd.read_stata(r"C:/Users/behri/OneDrive/Desktop/Master LSE/Essay/Ideas/Pepsi Coke/demo.dta")

data_address = data_demographics[["store", "lat", "long"]].dropna()
data_address["long"] = -data_address["long"]

# Convert into correct floats
data_address[["lat", "long"]] = data_address[["lat", "long"]] / 10000
data_address = data_address.rename(columns={"lat": "Latitude", "long": "Longitude"})

## Encode target location (bottling company)
target_address = "650 W 51st St, Chicago, IL 60609, USA"

geolocator = Nominatim(user_agent= "distance-app")
target_location = geolocator.geocode(target_address)

target = (target_location.latitude, target_location.longitude)

## Compute the distance to the target for each store 
distances = []

def compute_distance(row): 
    store_coords = (row["Latitude"], row["Longitude"])
    return geodesic(store_coords, target).miles

data_address["Distance"] = data_address.apply(compute_distance, axis = 1)

data_address.to_csv(r"C:/Users/behri/OneDrive/Desktop/Master LSE/Essay/Ideas/Pepsi Coke/distance_data.csv")
