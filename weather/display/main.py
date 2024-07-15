#!/usr/env/bin python

"""
Recieves weather data from the weather service
and displays it on an LCD. 
"""

import time
import pytz
import json
import socket
import logging
from datetime import datetime

import smbus2
from RPLCD.i2c import CharLCD


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger('display service')


# LCD configuration
I2C_ADDR = 0x27
LCD_COLUMNS = 20
LCD_ROWS = 4

lcd = CharLCD(i2c_expander='PCF8574', address=I2C_ADDR, port=1,
              cols=LCD_COLUMNS, rows=LCD_ROWS, charmap='A02',
              auto_linebreaks=True)


def format_message(raw_message: str, num_rows: int = 4, num_cols: int = 20) -> str:
    """
    Convert text to matrix format ideal for displaying
    on an LCD screen.

    Args:
        raw_message (str): The message without formatting. Use newline
                           characters for new lines on the LCD.
        num_rows (int): The number of rows available for the screen.
        num_cols (int): The number of columns available for the screen.

    Returns:
        str: A single string replacing new lines with the number of spaces
             needed to get to the end of the LCD row.
    """
    data = [[" "] * num_cols for _ in range(num_rows)]
    lines = raw_message.split("\n")

    if len(lines) > num_rows:
        raise ValueError(f"Can display up to {num_rows} lines. Got {len(lines)}")

    for i, line in enumerate(lines):
        if len(line) > num_cols:
            raise ValueError(f"Can display up to {num_cols} characters per line. Got {len(line)} on line {i}")

        # Fill the row with characters from the line
        for j, char in enumerate(line):
            data[i][j] = char

    formatted_message = "".join("".join(row) for row in data)
    return formatted_message


def receive_weather_data(host: str, port: int) -> None:
    """
    Receives weather data from a TCP connection,
    sends a confirmation, and displays the data on
    the LCD screen.

    Args:
        host (str): The hostname or IP address to bind to.
        port (int): The port number to bind to.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen(1)
        logger.info(f"Listening on {host}:{port}")

        while True:
            conn, addr = sock.accept()
            with conn:
                logger.info(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break

                    weather_data = json.loads(data.decode('utf-8'))
                    logger.info(f"Recieved data: {weather_data}")

                    temp = weather_data["temperature"]
                    temp_unit = weather_data["temperature_unit"]
                    now = datetime.now()
                    la_time = datetime.now(
                        pytz.timezone('America/Los_Angeles')
                    ).strftime("%H:%M:%S")


                    lcd.clear()
                    lcd.write_string(
                            format_message(f"Temp: {temp}o {temp_unit}\nUpdated: {la_time}")
                    )

                    conn.sendall(b"Data received")


def main():
    host = '0.0.0.0'
    port = 55000
    receive_weather_data(host, port)


if __name__ == "__main__":
    main()

