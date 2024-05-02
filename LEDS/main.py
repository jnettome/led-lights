
from ledstrip import LEDStrip
from ledcontroller import LEDController

# GPIO pins for CLK and DAT
CLK = 13
DAT = 12

if __name__ == "__main__":
    led_controller = LEDController(CLK, DAT, debug=True)
    led_controller.run()