const express = require('express');
const app = express();
const port = 3000; // Port where the server will listen

const LEDController = require('./ledcontroller.js');
const controller = new LEDController(33, 32, false);

controller.run(); // Start the mode run loop

// Endpoint to switch LED mode
app.get('/switch-mode', (req, res) => {
    controller.switchMode();
    res.send('Mode switched!');
});

// Start the server
app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});

process.on('SIGINT', () => {
    console.log('Program exited gracefully.');
    controller.cleanup();
    process.exit();
});
