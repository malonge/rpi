#!/bin/bash

import argparse
import threading
from time import sleep

from gpiozero import LED

"""
This module controls an LED connected to a Raspberry
Pi, allowing it to blink at user-specified intervals.

The script uses multithreading to enable continuous LED
blinking while concurrently waiting for user input to
terminate the program gracefully.
"""

stop_blinking = threading.Event()


def blink_led(interval: float) -> None:
    """
    Function to blink the LED at a specified interval.

    Args:
        interval (float): Time interval in seconds between LED state changes.
    """
    led = LED(17)
    while not stop_blinking.is_set():
        led.on()
        sleep(interval)
        led.off()
        sleep(interval)
    led.close()


def prompt_user() -> None:
    """
    Function to prompt the user to quit the program.
    """
    input("Press Enter to quit ...\n")
    print("Shutting down ...")
    stop_blinking.set()


def main() -> None:
    """
    Main function to start the LED blinking and user prompt threads.
    """
    parser = argparse.ArgumentParser(description='Blink an LED at a specified interval.')
    parser.add_argument(
        '-s',
        '--seconds',
        metavar="FLOAT",
        type=float,
        default=1.0,
        help='Interval in seconds for blinking the LED [1.0]'
    )
    args = parser.parse_args()

    blinking_thread = threading.Thread(target=blink_led, args=(args.seconds,))
    blinking_thread.start()

    input_thread = threading.Thread(target=prompt_user)
    input_thread.start()

    blinking_thread.join()
    input_thread.join()

    print("Goodbye")

if __name__ == "__main__":
    main()

