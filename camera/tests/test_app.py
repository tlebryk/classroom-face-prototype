import pytest
import sys
from app import (
    call_ml_service,
    query_student_db,
    update_frontend,
    process_capture,
    main,
)


# Dummy response class for simulating requests responses.
class DummyResponse:
    def __init__(self, status_code, json_data, text=""):
        self.status_code = status_code
        self._json = json_data
        self.text = text

    def json(self):
        return self._json


# -------- Tests for call_ml_service --------


def test_call_ml_service_success(monkeypatch):
    # Simulate a successful ML service response.
    def dummy_post(url, json):
        return DummyResponse(
            200,
            {
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
            },
        )

    monkeypatch.setattr("app.requests.post", dummy_post)
    result = call_ml_service("dummy_image")
    assert result["FaceMatches"][0]["Face"]["ExternalImageId"] == "stu123"


def test_call_ml_service_failure(monkeypatch):
    # Simulate a failure (non-200 response) from the ML service.
    def dummy_post(url, json):
        return DummyResponse(500, None, "ML Service error occurred")

    monkeypatch.setattr("app.requests.post", dummy_post)
    with pytest.raises(Exception) as excinfo:
        call_ml_service("dummy_image")
    assert "ML Service error" in str(excinfo.value)


# -------- Tests for query_student_db --------


def test_query_student_db_success(monkeypatch):
    def dummy_get(self, url, **kwargs):
        # Include self parameter to match the Session.get method signature
        return DummyResponse(
            200,
            {
                "studentId": "stu123",
                "name": "Alice Johnson",
                "email": "alice@example.com",
                "photoReference": "ref1",
            },
        )

    # This patches the Session.get method itself
    monkeypatch.setattr("requests.sessions.Session.get", dummy_get)

    result = query_student_db("stu123")
    assert result["name"] == "Alice Johnson"


def test_query_student_db_failure(monkeypatch):
    def dummy_get(self, url, **kwargs):
        # Include self parameter and use **kwargs
        return DummyResponse(404, None, "Student not found")

    monkeypatch.setattr("requests.sessions.Session.get", dummy_get)
    with pytest.raises(Exception) as excinfo:
        query_student_db("stu123")
    assert "Student DB error" in str(excinfo.value)


# -------- Tests for update_frontend --------


def test_update_frontend_success(monkeypatch):
    def dummy_post(url, json):
        return DummyResponse(200, {"message": "Update successful"})

    monkeypatch.setattr("app.requests.post", dummy_post)
    payload = {
        "studentId": "stu123",
        "name": "Alice Johnson",
        "seatId": "seat5",
        "confidence": 0.998,
        "lastSeen": "dummy",
    }
    result = update_frontend(payload)
    assert result["message"] == "Update successful"


def test_update_frontend_failure(monkeypatch):
    def dummy_post(url, json):
        return DummyResponse(500, None, "Update failed")

    monkeypatch.setattr("app.requests.post", dummy_post)
    payload = {
        "studentId": "stu123",
        "name": "Alice Johnson",
        "seatId": "seat5",
        "confidence": 0.998,
        "lastSeen": "dummy",
    }
    with pytest.raises(Exception) as excinfo:
        update_frontend(payload)
    assert "Frontend UI error" in str(excinfo.value)


# -------- Tests for process_capture --------


# Dummy functions to simulate a full successful flow.
def dummy_ml_success(image_data):
    return {
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


def dummy_student_success(student_id):
    return {
        "studentId": "stu123",
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "photoReference": "ref1",
    }


def dummy_frontend_success(payload):
    return {"message": "Update successful"}


def test_process_capture_success(monkeypatch):
    monkeypatch.setattr("app.call_ml_service", dummy_ml_success)
    monkeypatch.setattr("app.query_student_db", dummy_student_success)
    monkeypatch.setattr("app.update_frontend", dummy_frontend_success)

    result, status = process_capture("dummy_image")
    assert status == 200
    assert result["student_data"]["name"] == "Alice Johnson"
    assert result["frontend_update"]["seatId"] == "seat5"
    assert result["message"] == "Capture and update successful"


def test_process_capture_ml_failure(monkeypatch):
    def dummy_ml_failure(image_data):
        raise Exception("ML Service error: Service unreachable")

    monkeypatch.setattr("app.call_ml_service", dummy_ml_failure)
    result, status = process_capture("dummy_image")
    assert status == 500
    assert "error" in result
    assert "ML Service error" in result["error"]


# -------- Test for main() --------


def test_main_success(monkeypatch, capsys):
    # Patch process_capture so that main() returns a known result.
    def dummy_process_capture(image_data):
        return {"result": "test success"}, 0

    monkeypatch.setattr("app.process_capture", dummy_process_capture)
    # Simulate passing an argument (or not, since "dummy" is default).
    monkeypatch.setattr(sys, "argv", ["app.py", "dummy_image"])
    with pytest.raises(SystemExit) as excinfo:
        main()
    # main() calls sys.exit with the status code.
    assert excinfo.value.code == 0
    captured = capsys.readouterr().out
    assert "Status: 0" in captured
    assert "test success" in captured
