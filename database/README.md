# Classroom Facial Recognition System - Database Service

This service provides a lightweight REST API to interact with a SQLite database that stores student information. It is part of the prototype system to map student identities to seating positions in a classroom.

## Features

- **GET /api/student**: Retrieve student details by `studentId`
- **POST /api/student**: Add a new student record
- **GET /api/health**: Check database status and get student count
- Automated initialization with student records from JSON file
- Integrated image management for face recognition
- Built with Flask and SQLite

## Database Preparation Process

The database service uses a two-part automated setup process:

### 1. Student Information from students.json

The `students.json` file contains the metadata for all students in a structured format:

```json
[
  {
    "studentId": "jayvin",
    "name": "Jayvin Smith",
    "email": "jayvin@example.com", 
    "photoReference": "jayvin.jpg"
  },
  ...
]
```

### 2. Student Images from db_images/

The `db_images/` directory contains the actual image files for all students:
- jayvin.jpg
- enrique.png
- michelle.jpg
- etc.

### 3. Automated Setup on Startup

When the service starts:
1. It reads the `students.json` file to get student information
2. Loads student records into the SQLite database
3. Takes the images from `db_images/` and processes them
4. Copies the images to a shared volume for the ML service to access

**Important:** The `photoReference` value in the JSON must match the filename in the `db_images/` directory for proper association.

## How It Works

### 1. Student Data Management

The database service stores student information including:
- Student ID
- Name
- Email
- Photo reference (filename of the student's image)

### 2. Automated Setup

On startup, the service:
1. Reads student information from `students.json`
2. Creates student records in the SQLite database 
3. Copies student images from `db_images/` to a shared directory
4. Makes the images available to the ML service

### 3. Integration with ML Service

- Images processed by the database service are shared with the ML service
- The ML service uses these images as reference faces for recognition
- When a face is recognized, the ML service queries this database for complete student information

## Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- GNU Make (optional)

## Getting Started

### 1. Prepare Student Data

1. **Add student information to `students.json`**:
   ```json
   [
     {
       "studentId": "jayvin",
       "name": "Jayvin Smith",
       "email": "jayvin@example.com",
       "photoReference": "jayvin.jpg"
     },
     ...
   ]
   ```

2. **Add student images to `db_images/` directory**:
   - Ensure filenames match the `photoReference` values in students.json
   - Supported formats: jpg, jpeg, png
   - Example: If students.json has "photoReference": "jayvin.jpg", then db_images/ should contain jayvin.jpg

### 2. Build and Run the Service

Using Docker Compose (recommended):
```bash
docker-compose up database
```

Using the Makefile:
```bash
cd database
make build
make run
```

### 3. Testing the API

Check if the service is running:
```bash
curl http://localhost:5002/api/health
```

Get an existing student:
```bash
curl -X GET "http://localhost:5002/api/student?studentId=jayvin"
```

Add a new student:
```bash
curl -X POST "http://localhost:5002/api/student" \
  -H "Content-Type: application/json" \
  -d '{"studentId": "newstudent", "name": "New Student", "email": "new@example.com", "photoReference": "newstudent.jpg"}'
```

Run all integration tests:
```bash
make test-curl
```

## API Reference

### GET /api/health
Returns the status of the database service.

**Response:**
```json
{
  "status": "ok",
  "student_count": 6
}
```

### GET /api/student?studentId={id}
Retrieves a student by ID.

**Response:**
```json
{
  "studentId": "jayvin",
  "name": "Jayvin Smith",
  "email": "jayvin@example.com",
  "photoReference": "jayvin.jpg"
}
```

### POST /api/student
Adds a new student record.

**Request Body:**
```json
{
  "studentId": "newstudent",
  "name": "New Student",
  "email": "new@example.com",
  "photoReference": "newstudent.jpg"
}
```

**Response:**
```json
{
  "message": "Student added successfully"
}
```

## Integration with ML Service

The database service shares processed images with the ML service through a Docker volume. This integration enables:

1. **Centralized Management**: Student information and reference images managed in one place
2. **Consistent Data**: ML service always has access to the latest student images
3. **Automated Setup**: No manual copying of files between services needed

## Configuration

The service can be configured with environment variables:

- `DATABASE_PATH`: Path to the SQLite database file (default: "students.db")
- `STUDENTS_JSON`: Path to the JSON file with student information (default: "students.json")
- `IMAGES_DIR`: Directory containing source images (default: "/app/db_images")
- `IMAGES_OUTPUT_DIR`: Directory to copy images to (default: "/app/images")

## Docker Volumes

- **database-images**: Shared volume between database and ML service for student images

## TODO:
Add our real records to this database.
Optional:
    - Add table layout table.
    - Figure out student pictures