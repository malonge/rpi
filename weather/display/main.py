#!/usr/env/bin python

"""
Recieves weather data from the weather service
and displays it on an LCD. 
"""

import time

import smbus2
from RPLCD.i2c import CharLCD

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


def main():
    while True:
        message = "temp: XZY F\nrel humidity: XZY\nAQI: XYZ"
        lcd.clear()
        lcd.write_string(format_message(message))

        time.sleep(10)
        lcd.clear()


if __name__ == "__main__":
    main()

