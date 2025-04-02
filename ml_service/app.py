# app.py
from flask import Flask, request, jsonify
import os
import logging
from utils import display_decoded_image, save_decoded_image, decode_image_to_rgb
from face_recognition import FaceRecognizer

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app = Flask(__name__)

reference_dir = os.environ.get("REFERENCE_FACES_DIR", "reference_faces")
similarity_threshold = float(os.environ.get("SIMILARITY_THRESHOLD", "0.6"))

database_url = os.environ.get("DATABASE_URL", "http://database:5002")

face_recognizer = FaceRecognizer(
    reference_dir=reference_dir,
    similarity_threshold=similarity_threshold,
    database_url=database_url,
)


@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        encoded_image = data.get("Image", {}).get("Bytes")

        if not encoded_image:
            app.logger.error("No image data found in the request.")
            return jsonify({"error": "No image data provided"}), 400

        saved_path = save_decoded_image(encoded_image)
        if saved_path:
            app.logger.info(f"Image saved for inspection at: {saved_path}")

        img_rgb = decode_image_to_rgb(encoded_image)
        if img_rgb is None:
            return jsonify({"error": "Failed to decode image"}), 400

        result = face_recognizer.recognize_face(img_rgb)

        return jsonify(result)

    except Exception as e:
        app.logger.error(f"Error in prediction: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "database_size": len(face_recognizer.db_names)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
