from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json()
    # Here we ignore actual ML logic and return a dummy response.
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
