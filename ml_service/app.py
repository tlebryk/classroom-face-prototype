# app.py
from flask import Flask, request, jsonify
from utils import display_decoded_image, save_decoded_image

app = Flask(__name__)


@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json()
    # Extract the base64 encoded image from the payload
    encoded_image = data.get("Image", {}).get("Bytes")
    if encoded_image:
        # Save the decoded image to a file for debugging/inspection
        saved_path = save_decoded_image(encoded_image)
        if saved_path:
            app.logger.info(f"Image saved for inspection at: {saved_path}")
        else:
            app.logger.error("Image could not be saved.")
    else:
        app.logger.error("No image data found in the request.")

    # Dummy ML logic for demonstration purposes.
    response = {
        "FaceMatches": [
            {
                "Similarity": 98.9,
                "Face": {
                    "FaceId": "f0a1b2c3",
                    "ExternalImageId": "stu123",
                    "Confidence": 99.8,
                },
            }
        ]
    }
    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
