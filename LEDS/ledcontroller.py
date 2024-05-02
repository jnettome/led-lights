import time
import math

from ledstrip import LEDStrip
import os

class LEDController:
    def __init__(self, clk_pin, dat_pin, debug=False):
        self.debug = debug
        self.MODES = {"STATIC_COLOR": 1, "COLOR_CYCLE": 2, "BREATHING": 3}
        self.mode = self.MODES["STATIC_COLOR"]  # Initial mode

        # Color definitions
        self.static_color = [255, 20, 147]  # DeepPink
        self.cycle_colors = [[255, 87, 51], [227, 11, 92], [64, 224, 208]]
        self.color_index = 0
        self.color_change_interval = 5  # Interval in seconds
        self.last_color_change_time = time.time()

        # Breathing mode
        self.breath_cycle_duration = 7  # Duration in seconds

        # Flag to track if static color has been set
        self.color_set = False

        # Only initialize the LEDStrip if not in debug mode
        if not self.debug:
            self.strip = LEDStrip(clk_pin, dat_pin)
        else:
            print("Debug mode active: LEDStrip hardware initialization skipped.")

    def switch_mode(self):
        self.mode = (self.mode % 3) + 1
        print(f"Mode switched to {'STATIC_COLOR' if self.mode == self.MODES['STATIC_COLOR'] else 'COLOR_CYCLE' if self.mode == self.MODES['COLOR_CYCLE'] else 'BREATHING'}.")

    def static_color_mode(self):
        if not self.color_set:
            hex_color = "#{:02x}{:02x}{:02x}".format(*self.static_color)
            print("\033[48;2;{};{};{}m Static color set to: {} \033[0m".format(*self.static_color, hex_color))
            if not self.debug:
                self.strip.setcolourrgb(*self.static_color)
            self.color_set = True

    def color_cycle_mode(self):
        current_time = time.time()
        if current_time - self.last_color_change_time > self.color_change_interval:
            self.last_color_change_time = current_time
            start_color = self.cycle_colors[self.color_index]
            self.color_index = (self.color_index + 1) % len(self.cycle_colors)
            end_color = self.cycle_colors[self.color_index]
            duration = 5  # Duration of color transition in seconds
            transition_interval = 0.05  # Interval for color transition in seconds
            steps = int(duration / transition_interval)
            for step in range(steps + 1):
                ratio = step / steps
                transition_color = [int(start + (end - start) * ratio) for start, end in zip(start_color, end_color)]
                hex_color = "#{:02x}{:02x}{:02x}".format(*transition_color)
                print("\033[48;2;{};{};{}m Color transitioned to: {} \033[0m".format(*transition_color, hex_color))
                if not self.debug:
                    self.strip.setcolourrgb(*transition_color)
                time.sleep(transition_interval)

    def breathing_mode(self):
        current_time = time.time()
        time_into_cycle = (current_time % self.breath_cycle_duration) / self.breath_cycle_duration
        brightness = (math.sin(time_into_cycle * 2 * math.pi) + 1) / 2
        adjusted_color = [int(c * brightness) for c in self.cycle_colors[0]]
        hex_color = "#{:02x}{:02x}{:02x}".format(*adjusted_color)
        print("\033[48;2;{};{};{}m Breathing mode: brightness {:.2f}, color: {} \033[0m".format(*adjusted_color, brightness, hex_color))
        if not self.debug:
            self.strip.setcolourrgb(*adjusted_color)

    def run(self):
        try:
            while True:
                # check if a temp file exists to change mode
                try:
                    with open("temp.txt", "r") as f:
                        self.switch_mode()
                        f.close()
                        # remove the temp file
                        os.remove("temp.txt")
                except FileNotFoundError:
                    pass

                if self.mode == self.MODES["STATIC_COLOR"]:
                    self.static_color_mode()
                    time.sleep(1)
                elif self.mode == self.MODES["COLOR_CYCLE"]:
                    self.color_cycle_mode()
                    time.sleep(1)
                elif self.mode == self.MODES["BREATHING"]:
                    self.breathing_mode()
                    time.sleep(0.1)
        except KeyboardInterrupt:
            print("Program exited gracefully")
        finally:
            if not self.debug:
                self.strip.cleanup()