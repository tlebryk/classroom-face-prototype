import os
import tempfile
import sqlite3
import json
import pytest
from app import app, init_db


@pytest.fixture
def client():
    # Use a temporary file for the test database
    db_fd, temp_db = tempfile.mkstemp()
    os.environ["DATABASE_PATH"] = temp_db
    init_db()  # Initialize the DB with our schema and sample data
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
    os.close(db_fd)
    os.remove(temp_db)


def test_get_student_missing_param(client):
    response = client.get("/api/student")
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_get_existing_student(client):
    response = client.get("/api/student?studentId=stu123")
    assert response.status_code == 200
    data = response.get_json()
    assert data["studentId"] == "stu123"
    assert data["name"] == "Alice Johnson"


def test_add_student_success(client):
    new_student = {
        "studentId": "stu456",
        "name": "Bob Smith",
        "email": "bob@example.com",
        "photoReference": "ref2",
    }
    response = client.post("/api/student", json=new_student)
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Student added successfully"

    # Verify via a GET request
    get_response = client.get("/api/student?studentId=stu456")
    assert get_response.status_code == 200
    get_data = get_response.get_json()
    assert get_data["name"] == "Bob Smith"


def test_add_duplicate_student(client):
    duplicate_student = {
        "studentId": "stu123",
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "photoReference": "ref1",
    }
    response = client.post("/api/student", json=duplicate_student)
    assert response.status_code == 409
    data = response.get_json()
    assert "error" in data
