#!/usr/bin/python

"""
LEDStrip Class

A Python class for controlling an Open-Smart RGB LED Strip from a Raspberry Pi.
Hardware source: http://www.dx.com/p/full-color-rgb-led-strip-driver-module-for-arduino-blue-black-314667
Original developer: Philip Leder (https://github.com/schlank/Catalex-Led-Strip-Driver-Raspberry-Pi)

Usage:
- Place this file in the same directory as your code.
- In your code, import this module and create an instance of LEDStrip with the chosen GPIO pins for CLK and DAT.
- Use the methods provided to set the color of the LED strip.

Example:
    from ledstrip import LEDStrip
    CLK = 17
    DAT = 18
    strip = LEDStrip(CLK, DAT)
    strip.setcolourrgb(255, 0, 0)  # Set color to red
"""

import time
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

class LEDStrip:
    def __init__(self, clock, data):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.__clock = clock
        self.__data = data
        self.__delay = 0.0001  # Add a small delay to stabilize signal
        GPIO.setup(self.__clock, GPIO.OUT)
        GPIO.setup(self.__data, GPIO.OUT)

    def __sendclock(self):
        GPIO.output(self.__clock, False)
        time.sleep(self.__delay)
        GPIO.output(self.__clock, True)
        time.sleep(self.__delay)

    def __send32zero(self):
        for _ in range(32):
            GPIO.output(self.__data, False)
            self.__sendclock()

    def __senddata(self, dx):
        self.__send32zero()
        for _ in range(32):
            GPIO.output(self.__data, True if (dx & 0x80000000) else False)
            dx <<= 1
            self.__sendclock()
        self.__send32zero()

    def __getcode(self, dat):
        return ((0x02 if (dat & 0x80) == 0 else 0) | 
                (0x01 if (dat & 0x40) == 0 else 0))

    def setcolourrgb(self, red, green, blue):
        dx = (0x03 << 30) | (self.__getcode(blue) << 28) | (self.__getcode(green) << 26) | (self.__getcode(red) << 24)
        dx |= (blue << 16) | (green << 8) | red
        self.__senddata(dx)

    def setcolourwhite(self):
        self.setcolourrgb(255, 255, 255)

    def setcolouroff(self):
        self.setcolourrgb(0, 0, 0)

    def setcolourred(self):
        self.setcolourrgb(255, 0, 0)

    def setcolourgreen(self):
        self.setcolourrgb(0, 255, 0)

    def setcolourblue(self):
        self.setcolourrgb(0, 0, 255)

    def setcolourhex(self, hex):
        try:
            hexcolour = int(hex, 16)
            self.setcolourrgb((hexcolour >> 16) & 0xFF, (hexcolour >> 8) & 0xFF, hexcolour & 0xFF)
        except ValueError:
            print(f"Error converting Hex input ({hex}) to a color.")

    def cleanup(self):
        self.setcolouroff()
        GPIO.cleanup()
