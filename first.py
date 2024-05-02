from flask import Flask, request, jsonify
import time
import math
from ledstrip import LEDStrip

app = Flask(__name__)

# GPIO pins for CLK and DAT
CLK = 13
DAT = 12

# Create an LEDStrip instance
strip = LEDStrip(CLK, DAT)

# Modes of operation
class Mode:
    STATIC_COLOR = 1
    COLOR_CYCLE = 2
    BREATHING = 3

mode = Mode.STATIC_COLOR  # Initial mode

# Color definitions
staticColor = (255, 20, 147)  # DeepPink
cycleColors = [(255, 87, 51), (227, 11, 92), (64, 224, 208)]
colorIndex = 0
colorChangeInterval = 5  # Interval in seconds
lastColorChangeTime = time.time()

@app.route('/health.json', methods=['GET'])
def health():
    return jsonify({
        'mode': mode,
        'staticColor': f'#{staticColor[0]:02x}{staticColor[1]:02x}{staticColor[2]:02x}',
        'cycleColors': [f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}' for color in cycleColors]
    })

@app.route('/change_mode.json', methods=['POST'])
def change_mode():
    global mode
    mode = (mode % 3) + 1
    return jsonify({'new_mode': mode})

@app.route('/change_static_color.json', methods=['POST'])
def change_static_color():
    global staticColor
    color_hex = request.json.get('color', '')
    staticColor = tuple(int(color_hex[i:i+2], 16) for i in (1, 3, 5))
    strip.setcolourrgb(*staticColor)
    return jsonify({'new_static_color': color_hex})

@app.route('/change_cycle_colors.json', methods=['POST'])
def change_cycle_colors():
    global cycleColors
    colors_hex = request.json.get('colors', '')
    cycleColors = [tuple(int(color[i:i+2], 16) for i in (1, 3, 5)) for color in colors_hex.split(',')]
    return jsonify({'new_cycle_colors': colors_hex})

def main_loop():
    try:
        while True:
            if mode == Mode.STATIC_COLOR:
                strip.setcolourrgb(*staticColor)
            elif mode == Mode.COLOR_CYCLE:
                strip.setcolourrgb(*cycleColors[colorIndex])
            elif mode == Mode.BREATHING:
                adjustedColor = tuple(int(c * ((math.sin(time.time() * math.pi / 3.5) + 1) / 2)) for c in cycleColors[0])
                strip.setcolourrgb(*adjustedColor)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program exited gracefully")

if __name__ == '__main__':
    from threading import Thread
    Thread(target=main_loop, daemon=True).start()
    app.run(debug=True, host='0.0.0.0')
