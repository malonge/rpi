#!/usr/bin/env python

import os

import requests

def get_nws_current_weather_data(latitude, longitude):
    # Construct the URL for the NWS API endpoint
    points_url = f"https://api.weather.gov/points/{latitude},{longitude}"
    
    # Get the station information
    points_response = requests.get(points_url)
    points_data = points_response.json()
    observation_stations_url = points_data['properties']['observationStations']
    
    # Get the list of observation stations
    stations_response = requests.get(observation_stations_url)
    stations_data = stations_response.json()
    observation_url = stations_data['features'][0]['id'] + "/observations/latest"
    
    # Get the latest observation data
    observation_response = requests.get(observation_url)
    observation_data = observation_response.json()
    
    # Extract relevant data
    temperature = observation_data['properties']['temperature']['value']
    humidity = observation_data['properties']['relativeHumidity']['value']
    description = observation_data['properties']['textDescription']
    
    return temperature, humidity, description

def get_airnow_aqi(api_key, latitude, longitude):
    url = "https://www.airnowapi.org/aq/observation/latLong/current"
    headers = {
        'Accept': 'application/json'  # Ensures the response is in JSON-LD format
    }

    params = {
        'format': 'application/json',
        'latitude': latitude,
        'longitude': longitude,
        'distance': 25,
        'API_KEY': api_key
    }
    print(params)
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    print(data)
    
    if response.status_code == 200 and data:
        aqi = data[1]['AQI']
        category = data[1]['Category']['Name']
        return aqi, category
    else:
        return None, None

latitude = "34.0928"  # Hollywood, CA latitude
longitude = "-118.3287"  # Hollywood, CA longitude
airnow_api_key = os.environ.get("AIRNOW_KEY", "")
if not airnow_api_key:
    raise RuntimeError("Missing AirNow API Key in AIRNOW_KEY env variable")

temperature, humidity, description = get_nws_current_weather_data(latitude, longitude)
aqi, category = get_airnow_aqi(airnow_api_key, latitude, longitude)

print(f"Temperature: {temperature}°C")
print(f"Humidity: {humidity}%")
print(f"Description: {description}")
print(f"AQI: {aqi} ({category})")

