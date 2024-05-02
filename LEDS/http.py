from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/switch-mode.json', methods=['GET'])
def switch_mode():
    # Create an empty text file called "temp.txt" in the current script location
    with open('temp.txt', 'w') as f:
        pass
    
    # Return a JSON response with success message
    return jsonify({"success": True}), 200

if __name__ == '__main__':
    app.run(debug=True)