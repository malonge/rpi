import time
import smbus2
from RPLCD.i2c import CharLCD

# The I2C address of the LCD
I2C_ADDR = 0x27

# Define the LCD parameters
LCD_COLUMNS = 20
LCD_ROWS = 4

# Initialize the I2C bus and LCD
lcd = CharLCD(i2c_expander='PCF8574', address=I2C_ADDR, port=1,
              cols=LCD_COLUMNS, rows=LCD_ROWS, charmap='A02',
              auto_linebreaks=True)

# Clear the LCD screen
lcd.clear()

# Display the message
lcd.write_string("Hello, World!")

# Keep the message on the screen for 10 seconds
time.sleep(1000)

# Optionally clear the display before exiting
lcd.clear()

