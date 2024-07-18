#!/usr/bin/env python

"""
Collects weather data from public APIs and
sends it to other services in the network.

The service currently gets basic data like
temperature and humidity from the National
Weather Service API.
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


class TCPConnection:
    """Manages a persistent TCP connection.

    Attributes:
        host (str): The host address to connect to.
        port (int): The port number to connect to.
        sock (socket.socket): The TCP socket object.
    """
    
    def __init__(self, host: str, port: int) -> None:
        """Initializes the TCPConnection with the specified host and port.

        Args:
            host (str): The host address to connect to.
            port (int): The port number to connect to.
        """
        self.host = host
        self.port = port
        self.sock: socket.socket | None = None
    
    def connect(self) -> None:
        """Establishes the TCP connection."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
    
    def send_data(self, data: str) -> None:
        """Sends data over the established TCP connection.

        Args:
            data (str): The data to send.
        """
        if self.sock:
            self.sock.sendall(data.encode('utf-8'))
    
    def close(self) -> None:
        """Closes the TCP connection."""
        if self.sock:
            self.sock.close()
            self.sock = None


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


def main():
    host = 'display'
    port = 55000
    interval = 300

    # Connect to the display service
    connection = TCPConnection(host, port)
    connection.connect()

    while True:
        temperature, humidity, description = get_nws_current_weather_data()
        data = {
            "temperature": temperature,
            "temperature_unit": "C",
            "humidity": humidity,
            "description": description
        }
        weather_json = json.dumps(data) 
        connection.send_data(weather_json)

        time.sleep(interval)

    connection.close()

if __name__ == "__main__":
    main()

