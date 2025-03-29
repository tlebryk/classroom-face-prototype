from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)
DATABASE = os.environ.get("DATABASE_PATH", "students.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (
            studentId TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            photoReference TEXT
        )
    """
    )
    # Insert a sample record if table is empty
    cursor.execute("SELECT COUNT(*) FROM students")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            """
            INSERT INTO students (studentId, name, email, photoReference)
            VALUES (?, ?, ?, ?)
        """,
            ("stu123", "Alice Johnson", "alice@example.com", "ref1"),
        )
    conn.commit()
    conn.close()


@app.route("/api/student", methods=["GET"])
def get_student():
    student_id = request.args.get("studentId")
    if not student_id:
        return jsonify({"error": "studentId parameter is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE studentId = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        student = dict(row)
        return jsonify(student)
    else:
        return jsonify({"error": "Student not found"}), 404


@app.route("/api/student", methods=["POST"])
def add_student():
    data = request.get_json()
    required_fields = ["studentId", "name", "email"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400
    student_id = data["studentId"]
    name = data["name"]
    email = data["email"]
    photoReference = data.get("photoReference", None)

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO students (studentId, name, email, photoReference)
            VALUES (?, ?, ?, ?)
        """,
            (student_id, name, email, photoReference),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Student already exists"}), 409
    conn.close()
    return jsonify({"message": "Student added successfully"}), 201


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
