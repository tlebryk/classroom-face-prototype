import pytest
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_predict_endpoint(client):
    payload = {
        "CollectionId": "student-gallery",
        "Image": {"Bytes": "base64encodeddummydata"},
        "MaxFaces": 1,
        "FaceMatchThreshold": 80,
    }
    response = client.post("/api/predict", json=payload)
    data = response.get_json()
    expected = {
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
    assert response.status_code == 200
    assert data == expected
