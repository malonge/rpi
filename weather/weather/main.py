#!/usr/bin/env python

import os
import json
import time
import logging
from typing import Tuple

import requests


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger('weather service')


def get_nws_current_weather_data(
    latitude: float,
    longitude: float
) -> Tuple[float, float, str]:
    """
    Get current weather data from the national weather
    service given coordinates.

    Args:
        latitude (float): Latitude for the location.
        longitude (float): Longitude for the location.
    Returns:
        Tuple[float, float, str]: A tuple of temperature, humidity, and 
            a description of the weather.
    """
    points_url = f"https://api.weather.gov/points/{latitude},{longitude}"
    
    # Stations
    points_response = requests.get(points_url)
    points_data = points_response.json()
    observation_stations_url = points_data['properties']['observationStations']
    
    stations_response = requests.get(observation_stations_url)
    stations_data = stations_response.json()
    observation_url = stations_data['features'][0]['id'] + "/observations/latest"
    
    # Get the latest observation data
    observation_response = requests.get(observation_url)
    observation_data = observation_response.json()
    
    temperature = observation_data['properties']['temperature']['value']
    humidity = observation_data['properties']['relativeHumidity']['value']
    description = observation_data['properties']['textDescription']
    
    return temperature, humidity, description


def get_airnow_aqi(
    api_key: str,
    latitude: float, 
    longitude: float
) -> Tuple[int, str]:
    """
    Fetches the current Air Quality Index (AQI) and category
    from the AirNow API for the specified latitude and longitude.

    Args:
        api_key (str): API key for the AirNow API.
        latitude (float): Latitude for the location.
        longitude (float): Longitude for the location.

    Returns:
        Tuple[int, str]: AQI value and category name.

    Raises:
        requests.exceptions.HTTPError: If the API request fails.
        ValueError: If the response data is empty or malformed.
    """
    url = "https://www.airnowapi.org/aq/observation/latLong/current"
    headers = {'Accept': 'application/json'}
    params = {
        'format': 'application/json',
        'latitude': latitude,
        'longitude': longitude,
        'distance': 25,
        'API_KEY': api_key
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    
    if data and len(data) > 1:
        aqi = data[1]['AQI']
        category = data[1]['Category']['Name']
        return aqi, category

    raise ValueError("Invalid response data")


def main():
    latitude = "34.0928"
    longitude = "-118.3287"
    airnow_api_key = os.environ.get("AIRNOW_KEY", "")
    if not airnow_api_key:
        raise RuntimeError("Missing AirNow API Key in AIRNOW_KEY env variable")

    while True:
        temperature, humidity, description = get_nws_current_weather_data(latitude, longitude)
        aqi, category = get_airnow_aqi(airnow_api_key, latitude, longitude)

        data = {
            "temperature": temperature,
            "humidity": humidity,
            "description": description,
            "aqi": aqi,
            "category": category
        }

        logger.info("Got the following weather data from the weather service: %s", json.dumps(data))
        time.sleep(300)


if __name__ == "__main__":
    main()

