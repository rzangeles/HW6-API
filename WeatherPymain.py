# HW6 - WeatherPy Rev1

# Dependencies

import numpy as np
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import requests as req
import random
import api_keys
import json
import citipy as city
import datetime

# Open Weather Map API Key

weather_key = api_keys.WEATHERKEY

# Generate 500 random lat and long but with the following qualification (balanced distribution
# from 0 to 90 and 0 to -90 for lat) and (balanced distribution from 0 to 180 and 0 to -180 for long)  

init_lat = []
init_long = []
final_city = []
final_country = []

for i in range(600):

    # Generate random lat/longs using random functions
    
    new_lat = random.randint(-90, 90) + random.random()
    new_long = random.randint(-180, 180) + random.random()
    init_lat.append(new_lat)
    init_long.append(new_long)

    # Use citypy function of nearest_city to identify the nearest cities associated to the random lat/longs
    # Append the final_city and final_country lists

    new_city = city.nearest_city(new_lat, new_long)
    final_city.append(new_city.city_name)
    final_country.append(new_city.country_code)

#print(init_lat)
#print(init_long)
#print(final_city)
#print(final_country)

# Create a new DataFrame to store the needed data of city and country

world_cities_sample_df = pd.DataFrame(final_city)
world_cities_sample_df = world_cities_sample_df.rename(columns={0:'City'})
world_cities_sample_df["Country"] = final_country
print(world_cities_sample_df.head(10))

# Remove duplicate cities on the data frame

world_cities_sample_df = world_cities_sample_df.drop_duplicates()

# Duplicate the world_cities DataFrame to iterate weather data

cities_temp = world_cities_sample_df

# Save weather data config information

url = "http://api.openweathermap.org/data/2.5/weather"

parameters = {'appid': weather_key,
          'q': '',
          'units': 'Imperial'}

weather_data = []

# Loop through the list of cities and perform a request for data on each

for index, city in cities_temp.iterrows():
    # Get weather data
    parameters['q'] = city["City"] + "," + city["Country"] 
    response = req.get(url, params=parameters, ).json()
    
    # Print of each city as they are getting processed

    print(city["City"])
    print(url + "?appid=" + weather_key + "&q=" + str(city["City"])+ "," + str(city["Country"])+
             "&units=" + "Imperial") 

    if response["cod"] == 200:

        weather_data.append(response)

    else:

        # Remove the city from the main data frame

        world_cities_sample_df = world_cities_sample_df.loc[world_cities_sample_df["City"] != city["City"]]


print(json.dumps(weather_data, indent=4, sort_keys=True))

# Collect Needed Data and store to the final data frame

# Latitude
lat = []

# Longitude
lng = []

# Temperature in F (Imperial)
temperature = []

# Humidity in %
humidity = []

# Cloudiness in %
cloudiness = []

# Wind Speed in mph (Imperial)
wind_speed = []

# Loop through weather data, collect required data, and append the appropriate lists
for data in weather_data:

    lat.append(data['coord']['lat'])
    lng.append(data['coord']['lon'])
    temperature.append(data['main']['temp_max'])
    humidity.append(data['main']['humidity'])
    cloudiness.append(data['clouds']['all'])
    wind_speed.append(data['wind']['speed'])
    
#Store new data to the cities data frame

world_cities_sample_df["Latitude"] = lat
world_cities_sample_df["Longitude"] = lng
world_cities_sample_df['Temperature'] = temperature
world_cities_sample_df['Humidity'] = humidity
world_cities_sample_df['Cloudiness'] = cloudiness
world_cities_sample_df['Wind Speed'] = wind_speed


print(world_cities_sample_df.head(10))

# Save the file to a csv file

world_cities_sample_df.to_csv("world_cities_weather.csv")

# Plot the Data in Scatter Plots

# Obtain today's date

today_date = datetime.date.today()

# Scatter Plot for Temperature vs Latitude

plt.scatter(lat, temperature, marker='o')
plt.grid(True)
plt.title("Temperature (F) vs Latitude " + str(today_date))
plt.ylabel("Temperature (F)")
plt.xlabel("Latitude")
plt.savefig("Temperature&Lat.png")
plt.show()

# Scatter Plot for Humidity vs Latitude

plt.scatter(lat, humidity, marker='o')
plt.grid(True)
plt.title("Humidity (%) vs Latitude " + str(today_date))
plt.ylabel("Humidity (%)")
plt.xlabel("Latitude")
plt.savefig("Humidity&Lat.png")
plt.show()

# Scatter Plot for Cloudiness vs Latitude

plt.scatter(lat, cloudiness, marker='o')
plt.grid(True)
plt.title("Cloudiness vs Latitude " + str(today_date))
plt.ylabel("Cloudiness")
plt.xlabel("Latitude")
plt.savefig("Cloudiness&Lat.png")
plt.show()

# Scatter Plot for Windspeed vs Latitude

plt.scatter(lat, wind_speed, marker='o')
plt.grid(True)
plt.title("Wind Speed vs Latitude " + str(today_date))
plt.ylabel("Wind Speed (mph)")
plt.xlabel("Latitude")
plt.savefig("WindSpeed&Lat.png")
plt.show()