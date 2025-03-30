# app.py
from flask import Flask, request, jsonify
from utils import display_decoded_image

app = Flask(__name__)


@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json()
    # Here we ignore actual ML logic and return a dummy response.
    # if os.environ.get("DEBUG", "false").lower() == "true":
    # Attempt to decode and display the image for sanity checking
    encoded_image = data.get("Image", {}).get("Bytes")
    if encoded_image:
        display_decoded_image(encoded_image)
    else:
        print("No image data found in the request.")
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
