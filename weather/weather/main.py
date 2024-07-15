#!/usr/bin/env python

"""
Collects weather data from public APIs and
sends it to other services in the network.

The service currently gets basic data like
temperature, humidity, and AQI.
"""

import os
import json
import time
import socket
import logging
from typing import Tuple

import requests


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger('weather service')


def get_nws_current_weather_data() -> Tuple[float, float, str]:
    """
    Get current weather data from the national weather
    service Downtown Los Angeles station (FHMC1).

    Returns:
        Tuple[float, float, str]: A tuple of temperature, humidity, and 
            a description of the weather.
    """
    observation_url = "https://api.weather.gov/stations/FHMC1/observations/latest"
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
    
    if data:
        aqi = data[0]['AQI']
        category = data[0]['Category']['Name']
        return aqi, category

    raise ValueError("Invalid response data")


def send_weather_data_persistently(host, port, interval):
    """
    Send weather data to the display service at regular intervals over a persistent TCP connection.

    :param host: The hostname of the display service.
    :param port: The port number of the display service.
    :param interval: The interval (in seconds) at which to send the data.
    """
    while True:
        try:
            # Create a TCP/IP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))

            while True:
                # Generate and serialize the weather data
                airnow_api_key = os.environ.get("AIRNOW_KEY", "")
                if not airnow_api_key:
                    raise RuntimeError("Missing AirNow API Key in AIRNOW_KEY env variable")

                temperature, humidity, description = get_nws_current_weather_data()
                aqi, category = get_airnow_aqi(airnow_api_key, "34", "-118")

                data = {
                    "temperature": temperature,
                    "temperature_unit": "C",
                    "humidity": humidity,
                    "description": description,
                    "aqi": aqi,
                    "category": category
                }
                weather_json = json.dumps(data)

                # Send data
                sock.sendall(weather_json.encode('utf-8'))
                response = sock.recv(1024)
                logger.info(f"Received: {response.decode('utf-8')}")
                
                time.sleep(interval)

        except (socket.error, KeyboardInterrupt) as e:
            print(f"Connection error: {e}, retrying...")
            time.sleep(5)  # Wait before attempting to reconnect
            continue

        finally:
            sock.close()


def main():
    airnow_api_key = os.environ.get("AIRNOW_KEY", "")
    if not airnow_api_key:
        raise RuntimeError("Missing AirNow API Key in AIRNOW_KEY env variable")


    send_weather_data_persistently('display', 55000, interval=300)


if __name__ == "__main__":
    main()

