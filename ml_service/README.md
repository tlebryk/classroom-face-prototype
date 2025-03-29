# ML Service (DeepFace Mock)

This is a lightweight mock implementation of an ML prediction service for a classroom facial recognition system. It provides a `/api/predict` endpoint that accepts a properly formatted JSON request and returns a dummy face recognition response.

## Overview

- **Purpose:**  
  Mock the ML service that uses DeepFace (or Amazon Rekognition) for classroom facial recognition. Currently, the ML logic is bypassed in favor of a static response for integration testing.

- **Endpoint:**  
  - `POST /api/predict`  
    Expects a JSON payload with keys such as `CollectionId`, `Image`, `MaxFaces`, and `FaceMatchThreshold`.  
    Returns a JSON response with dummy face match data.

## Files

- **Dockerfile:**  
  Multi-stage Dockerfile with a tester stage for unit tests and a production stage running Gunicorn.
- **app.py:**  
  Flask application that defines the `/api/predict` endpoint.
- **requirements.txt:**  
  Python dependencies.
- **test_app.py:**  
  Pytest tests to validate the endpoint functionality.
- **Makefile:**  
  Commands to build, test, run, and perform integration testing with curl.

## Requirements

- Docker
- Make

## Usage

### Run Unit Tests

```bash
make test
```
This command builds the tester image and runs the Pytest tests.

Build and Run the Service
bash
Copy
make all
This command runs tests, builds the production image, and starts the container in detached mode. The service will be available at http://localhost:5000.

Integration Testing with Curl
bash
Copy
make test-curl
This sends a sample POST request to the /api/predict endpoint.

Stop the Service
bash
Copy
make stop
Stops and removes the running container.

Endpoint Example
Request:

json
Copy
POST /api/predict
{
  "CollectionId": "student-gallery",
  "Image": {
    "Bytes": "<base64-encoded-image>"
  },
  "MaxFaces": 1,
  "FaceMatchThreshold": 80
}
Response:

json
Copy
{
  "FaceMatches": [
    {
      "Similarity": 98.9,
      "Face": {
        "FaceId": "f0a1b2c3",
        "ExternalImageId": "stu123",
        "Confidence": 99.8
      }
    }
  ]
}

## TODO: 
implement real deepface