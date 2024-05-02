
import RPi.GPIO as GPIO
import time

class SoundDetector:
    def __init__(self, input_pin):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.__input_pin = input_pin
        GPIO.setup(self.__input_pin, GPIO.IN, initial=GPIO.LOW)

    def detect_sound(self):
        return GPIO.input(self.__input_pin)

    def cleanup(self):
        GPIO.cleanup()

# Example usage:
if __name__ == "__main__":
    INPUT_PIN = 17
    detector = SoundDetector(INPUT_PIN)
    try:
        while True:
            if detector.detect_sound():
                print("Sound detected!")
            else:
                print("No sound detected.")
            time.sleep(0.1)
    except KeyboardInterrupt:
        detector.cleanup()