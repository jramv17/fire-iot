from flask import Flask, jsonify
import threading
from fire_model import detect_fire

app = Flask(__name__)

@app.route("/api/detect-fire", methods=["GET"])
def detect_fire_api():
    # Call fire detection, allow up to 30 seconds
    fire = detect_fire(timeout=30)
    return jsonify({"fire_detected": fire})

if __name__ == "__main__":
    app.run(debug=True)
