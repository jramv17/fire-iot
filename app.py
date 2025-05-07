from flask import Flask, jsonify , request
from flask_cors import CORS
from fire_model import detect_fire
from fire_model_static import detect_fire_static
import os
import uuid
app = Flask(__name__)

@app.route("/api/detect-fire", methods=["GET"])
def detect_fire_api():
    # Call fire detection, allow up to 30 seconds
    fire = detect_fire(timeout=30)
    return jsonify({"fire_detected": fire})

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("static/results", exist_ok=True)

@app.route("/api/detect-fire-img", methods=["POST"])
def detect_fire_image_api():
    # Your image handling code here

    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files['image']
    filename = f"{uuid.uuid4().hex}.jpg"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    image_file.save(file_path)

    result = detect_fire_static(file_path)

    return jsonify({
        "fire_detected": result["fire_detected"],
        "fire_percentage": result["fire_percentage"],
        "image_result_url": request.host_url + result["image_path"]
    })


if __name__ == "__main__":
    app.run(debug=True)
