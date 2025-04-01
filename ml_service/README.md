# ML Service (DeepFace Face Recognition)

This service provides real-time facial recognition capabilities using DeepFace for the classroom facial recognition system. It analyzes images to identify students and retrieves their complete information from the database service.

## Overview

- **Purpose:**  
  Process images using DeepFace to identify students in a classroom setting, integrate with the database service to retrieve complete student information, and return comprehensive identification results.

- **Technology:**
  - DeepFace for facial recognition
  - ArcFace model for embedding extraction
  - Cosine similarity for face matching
  - Flask for API endpoints

- **Endpoints:**  
  - `POST /api/predict`  
    Analyzes an image to identify faces and match them against registered students.
  - `GET /api/health`  
    Returns the status of the ML service and information about loaded reference faces.

## Files

- **Dockerfile:**  
  Multi-stage Dockerfile with a tester stage for unit tests and a production stage running Gunicorn.
- **app.py:**  
  Flask application that defines the API endpoints.
- **face_recognition.py:**  
  Core ML functionality using DeepFace for facial recognition.
- **utils.py:**  
  Utility functions for image processing and base64 encoding/decoding.
- **requirements.txt:**  
  Python dependencies including DeepFace, TensorFlow, and Flask.
- **reference_faces/:**  
  Directory where reference face images are stored (shared with database service).

## Integration with Database Service

The ML service is designed to work seamlessly with the database service:

1. **Reference Images**: Uses reference face images maintained by the database service
2. **Student Lookup**: After recognizing a face, queries the database service for complete student information
3. **Shared Volume**: Uses a Docker volume to access images processed by the database service

### Image Storage and Access

It's important to understand how images are handled in the system:

- **Images are NOT stored in the database itself**:
  - The actual image files remain in the filesystem
  - The database only stores metadata, including the "photoReference" field

- **Image Flow**:
  1. Original images are placed in the `db_images/` directory in the database service
  2. On startup, the database service:
     - Reads `students.json` to get student records
     - Copies images from `db_images/` to a shared Docker volume
  3. The ML service reads these image files directly from the shared volume

- **Database Queries**:
  - When the ML service recognizes a face, it first identifies the studentId
  - Then it queries the database to get the complete student information
  - It doesn't get images from the database - it already has direct access to them

This approach provides better performance (images don't need to be transferred over API calls) and cleaner separation of concerns (database handles metadata, filesystem handles images).

```
File System:                      SQLite Database:
┌───────────────┐                ┌───────────────┐
│ db_images/    │                │  students     │
│ - jayvin.jpg  │                │ ┌───────────┐ │
│ - enrique.png │                │ │studentId  │ │
│ - etc...      │                │ │name       │ │
└───────┬───────┘                │ │email      │ │
        │                        │ │photoRef   │ │
        ▼                        │ └───────────┘ │
┌───────────────┐                └───────┬───────┘
│ Shared Volume │                        │
│ (images)      │                        │
└───────┬───────┘                        │
        │                                │
        ▼                                ▼
┌───────────────────────────────────────────────┐
│ ML Service                                    │
│ 1. Reads images from shared volume            │
│ 2. Generates face embeddings                  │
│ 3. Recognizes face -> Gets studentId          │
│ 4. Queries database for student information   │
└───────────────────────────────────────────────┘
```

## API Endpoints

### POST /api/predict

Analyzes an image to identify faces and match them against registered students.

**Request Format:**
```json
{
  "Image": {
    "Bytes": "<base64-encoded-image>"
  }
}
```

**Response Format (Match Found):**
```json
{
  "match": true,
  "similarity": 98.75,
  "studentId": "jayvin",
  "studentInfo": {
    "email": "jayvin@example.com",
    "name": "Jayvin Smith",
    "photoReference": "jayvin.jpg",
    "studentId": "jayvin"
  },
  "allScores": {
    "jayvin": 98.75,
    "enrique": 45.23,
    "michelle": 32.61
  }
}
```

**Response Format (No Match):**
```json
{
  "match": false,
  "similarity": 42.31,
  "message": "No face matched above the similarity threshold",
  "allScores": {
    "jayvin": 42.31,
    "enrique": 37.92
  }
}
```

### GET /api/health

Returns the status of the ML service and information about loaded reference faces.

**Response Format:**
```json
{
  "status": "ok",
  "database_size": 6,
  "database_url": "http://database:5002"
}
```

## Requirements

- Docker
- Make (optional)

## Usage

### Build and Run with Docker Compose

```bash
# Build and run all services including ML service
docker-compose up

# Build from scratch
docker-compose up --build

# Or build and run just the ML service
docker-compose up ml-service
```

### Running with Make

```bash
cd ml_service
make test    # Run unit tests
make build   # Build the Docker image
make run     # Run the service
make all     # Run tests, build, and start the service
```

### Testing the API

**Health Check:**
```bash
curl http://localhost:5001/api/health
```

**Face Recognition:**
```bash
# Recognize a face from a local image
curl -X POST \
  -H "Content-Type: application/json" \
  -d "{\"Image\": {\"Bytes\": \"$(base64 -i ./database/db_images/jayvin.jpg)\"} }" \
  http://localhost:5001/api/predict
```

## How It Works

1. **Embedding Extraction**:
   - Face images are processed using DeepFace with the ArcFace model
   - Each face is converted to a high-dimensional embedding vector

2. **One-Shot Learning**:
   - The system requires only one reference image per person
   - Reference images are processed into embeddings at startup

3. **Recognition Process**:
   - New face images are converted to embeddings
   - Cosine similarity is calculated between the new face and all reference faces
   - If similarity exceeds the threshold, a match is declared
   - The database is queried for complete student information

## Configuration

The service can be configured with environment variables:

- `REFERENCE_FACES_DIR`: Directory containing reference face images (default: "/app/reference_faces")
- `SIMILARITY_THRESHOLD`: Threshold for face recognition (0-1) (default: 0.6)
- `DATABASE_URL`: URL of the database service (default: "http://database:5002")