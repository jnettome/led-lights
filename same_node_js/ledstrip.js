const rpio = require('rpio');
const CLK_PIN = 13;
const DAT_PIN = 12;

// LEDStrip
class LEDStrip {
    constructor(clock, data, debug = false) {
        this.clockPin = clock;
        this.dataPin = data;
        this.delay = 0.0001; // Add a small delay to stabilize signal
        this.debug = debug;

        // Initialize GPIO pins
        rpio.init({ gpiomem: false, mapping: 'gpio'});
        rpio.open(this.clockPin, rpio.OUTPUT, rpio.LOW);
        rpio.open(this.dataPin, rpio.OUTPUT, rpio.LOW);
    }

    sendClock() {
        rpio.write(this.clockPin, rpio.LOW);
        setTimeout(() => {
            rpio.write(this.clockPin, rpio.HIGH);
            if (this.debug) {
                console.log('Clock pulse sent');
            }
        }, this.delay * 1000);
    }

    send32Zero() {
        for (let i = 0; i < 32; i++) {
            rpio.write(this.dataPin, rpio.LOW);
            this.sendClock();
        }
        if (this.debug) {
            console.log('32 zeros sent');
        }
    }

    sendData(dx) {
        if (this.debug) {
            console.log(`Sending data: ${dx.toString(16)}`);
        }
        this.send32Zero();
        for (let i = 0; i < 32; i++) {
            rpio.write(this.dataPin, (dx & 0x80000000) ? rpio.HIGH : rpio.LOW);
            dx <<= 1;
            this.sendClock();
        }
        this.send32Zero();
    }

    getCode(dat) {
        const code = ((dat & 0x80) === 0 ? 0x02 : 0) |
            ((dat & 0x40) === 0 ? 0x01 : 0);
        if (this.debug) {
            console.log(`Get code for data: ${dat.toString(16)} = ${code.toString(16)}`);
        }
        return code;
    }

    setColourRGB(red, green, blue) {
        let dx = (0x03 << 30) | (this.getCode(blue) << 28) | (this.getCode(green) << 26) | (this.getCode(red) << 24);
        dx |= (blue << 16) | (green << 8) | red;
        if (this.debug) {
            console.log(`Set RGB: Red=${red}, Green=${green}, Blue=${blue}, dx=${dx.toString(16)}`);
        }
        this.sendData(dx);
    }

    setColourWhite() {
        this.setColourRGB(255, 255, 255);
    }

    setColourOff() {
        this.setColourRGB(0, 0, 0);
    }

    setColourRed() {
        this.setColourRGB(255, 0, 0);
    }

    setColourGreen() {
        this.setColourRGB(0, 255, 0);
    }

    setColourBlue() {
        this.setColourRGB(0, 0, 255);
    }

    setColourHex(hex) {
        try {
            const hexcolour = parseInt(hex, 16);
            this.setColourRGB((hexcolour >> 16) & 0xFF, (hexcolour >> 8) & 0xFF, hexcolour & 0xFF);
            if (this.debug) {
                console.log(`Set hex color: ${hex}`);
            }
        } catch (error) {
            console.error(`Error converting Hex input (${hex}) to a color.`);
        }
    }

    cleanup() {
        this.setColourOff();
        rpio.close(this.clockPin);
        rpio.close(this.dataPin);
        if (this.debug) {
            console.log('GPIO cleaned up');
        }
    }
}

module.exports = LEDStrip;

// Usage example:
// const strip = new LEDStrip(CLK_PIN, DAT_PIN, true);
// strip.setColourRGB(255, 0, 0); // Set color to red
