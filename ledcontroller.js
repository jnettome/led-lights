const LEDStrip = require('./ledstrip.js'); // Import the LEDStrip class from your custom module
const chalk = require('chalk');

class LEDController {
    constructor(clockPin, dataPin, debug = false) {
        this.debug = debug;
        this.MODES = { STATIC_COLOR: 1, COLOR_CYCLE: 2, BREATHING: 3 };
        this.mode = this.MODES.STATIC_COLOR; // Initial mode

        // Color definitions
        this.staticColor = [255, 20, 147]; // DeepPink
        this.cycleColors = [[255, 87, 51], [227, 11, 92], [64, 224, 208]];
        this.colorIndex = 0;
        this.colorChangeInterval = 5000; // Interval in milliseconds
        this.lastColorChangeTime = Date.now();

        // Breathing mode
        this.breathCycleDuration = 7000; // Duration in milliseconds

        this.interval = null;

        // Flag to track if static color has been set
        this.colorSet = false;

        // Only initialize the LEDStrip if not in debug mode
        if (!this.debug) {
            this.strip = new LEDStrip(clockPin, dataPin);
        } else {
            console.log("Debug mode active: LEDStrip hardware initialization skipped.");
        }
    }

    switchMode() {
        this.mode = (this.mode % 3) + 1;
        console.log(`Mode switched to ${this.mode === this.MODES.STATIC_COLOR ? 'STATIC_COLOR' : this.mode === this.MODES.COLOR_CYCLE ? 'COLOR_CYCLE' : 'BREATHING'}.`);
    }

    staticColorMode() {
        // console.log("Executing Static Color Mode.");
        // console.log(`Static color set to: ${this.staticColor}.`);
        // if (!this.debug) {
        //     this.strip.setColourRGB(this.staticColor[0], this.staticColor[1], this.staticColor[2]);
        // }

        // console.log("Executing Static Color Mode.");
        if (!this.colorSet) {
            const hexColor = `#${this.staticColor.map(c => c.toString(16).padStart(2, '0')).join('')}`;
            console.log(chalk.bgHex(hexColor).white(` Static color set to: ${hexColor} `));
            if (!this.debug) {
                this.strip.setColourRGB(this.staticColor[0], this.staticColor[1], this.staticColor[2]);
            }
            this.colorSet = true;
        } else {
            // console.log("Static color mode already set. Skipping.");
        }
    }

    // colorCycleMode() {
    //     this.colorSet = false;
    //     const currentTime = Date.now();
    //     if (currentTime - this.lastColorChangeTime > this.colorChangeInterval) {
    //       this.lastColorChangeTime = currentTime;
    //       this.colorIndex = (this.colorIndex + 1) % this.cycleColors.length;
    //       const hexColor = `#${this.cycleColors[this.colorIndex].map(c => c.toString(16).padStart(2, '0')).join('')}`;
    //       console.log(chalk.bgHex(hexColor).white(` Color cycled to index ${this.colorIndex}, color ${hexColor} `));
    //       if (!this.debug) {
    //           this.strip.setColourRGB(this.cycleColors[this.colorIndex][0], this.cycleColors[this.colorIndex][1], this.cycleColors[this.colorIndex][2]);
    //       }
    //   }
    // }
    colorCycleMode() {
      this.colorSet = false;
      const currentTime = Date.now();
      if (currentTime - this.lastColorChangeTime > this.colorChangeInterval) {
          this.lastColorChangeTime = currentTime;
          const startColor = this.cycleColors[this.colorIndex];
          this.colorIndex = (this.colorIndex + 1) % this.cycleColors.length;
          const endColor = this.cycleColors[this.colorIndex];
          const duration = 5000; // Duration of color transition in milliseconds

          const transitionInterval = 50; // Interval for color transition in milliseconds
          const steps = duration / transitionInterval;
          let step = 0;

          const transition = setInterval(() => {
              step++;
              const ratio = step / steps;
              const transitionColor = startColor.map((channel, index) => {
                  const delta = endColor[index] - channel;
                  return Math.round(channel + delta * ratio);
              });
              if (this.mode === this.MODES.COLOR_CYCLE) {
                const hexColor = `#${transitionColor.map(c => c.toString(16).padStart(2, '0')).join('')}`;
                console.log(chalk.bgHex(hexColor).white(` Color transitioned to index ${this.colorIndex}, color ${hexColor} `));
                if (!this.debug) {
                    this.strip.setColourRGB(transitionColor[0], transitionColor[1], transitionColor[2]);
                }
              }

              if (step >= steps) {
                  clearInterval(transition);
              }
          }, transitionInterval);
      }
  }

    breathingMode() {
      this.colorSet = false;
      const currentTime = Date.now();
      const timeIntoCycle = (currentTime % this.breathCycleDuration) / this.breathCycleDuration;
      const brightness = (Math.sin(timeIntoCycle * 2 * Math.PI) + 1) / 2;
      const adjustedColor = this.cycleColors[0].map(c => Math.round(c * brightness));
      const hexColor = `#${adjustedColor.map(c => c.toString(16).padStart(2, '0')).join('')}`;
      console.log(chalk.bgHex(hexColor).white(` Breathing mode: brightness ${brightness.toFixed(2)}, color ${hexColor} `));
      if (!this.debug) {
          this.strip.setColourRGB(adjustedColor[0], adjustedColor[1], adjustedColor[2]);
      }
    }

    run() {
        this.interval = setInterval(() => {
            // console.log(`Current mode: ${this.mode === this.MODES.STATIC_COLOR ? 'STATIC_COLOR' : this.mode === this.MODES.COLOR_CYCLE ? 'COLOR_CYCLE' : 'BREATHING'}.`);
            switch (this.mode) {
                case this.MODES.STATIC_COLOR:
                    this.staticColorMode();
                    break;
                case this.MODES.COLOR_CYCLE:
                    this.colorCycleMode();
                    break;
                case this.MODES.BREATHING:
                    this.breathingMode();
                    break;
            }
        }, 100);
    }

    cleanup() {
        console.log('Cleaning up resources...');
        if (!this.debug) {
            try {
                clearInterval(this.interval);
                this.strip.setColourOff();
                this.strip.cleanup();
            } catch (error) {
                console.error('Error clearing interval or cleaning up LEDStrip.');
            }
        }
    }
}

module.exports = LEDController;
