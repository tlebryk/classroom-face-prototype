# Classroom Face Prototype

This project is a multi-service application that integrates a machine learning service, a frontend, a database, and a camera service for classroom face recognition.

## Services

- **ml_service**: Provides ML-based face detection/recognition (exposes HTTP endpoints on port 8000).
- **frontend**: Hosts the user interface and classroom updates (exposes HTTP endpoints on port 3000).
- **database**: Manages student data (exposes HTTP endpoints on port 5002).
- **camera**: A one-shot service that captures an image, processes it, and triggers updates in the other services.

## Prerequisites

- [Docker](https://www.docker.com/) installed and running.
- Basic familiarity with Docker and Docker Compose.

## Getting Started

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Build and run all services:**

   There are multiple ways to build and run the services:

   **Option 1:** Using Docker Compose directly (recommended):
   ```bash
   # Build and start all services
   docker-compose up
   
   # Or to rebuild from scratch:
   docker-compose up --build
   
   # To run in background mode:
   docker-compose up -d
   ```

   **Option 2:** Using Makefiles:
   ```bash
   make all
   ```
   
   **Option 3:** Run camera service which triggers the pipeline:
   ```bash 
   docker-compose run camera
   ```

3. **Running individual services:**

   You can also build or run services individually:

   - Using Docker Compose:
     ```bash
     docker-compose up ml-service
     docker-compose up database
     docker-compose up frontend
     ```

   - Using Makefiles:
     ```bash
     make ml_service
     make database
     make frontend
     make camera
     ```

## Testing the Services

After running `docker-compose up`, you can test each service individually using curl commands:

### ML Service Tests

```bash
# Test the ML service health endpoint
curl http://localhost:8000/api/health

# Test face recognition with a sample image
curl -X POST \
  -H "Content-Type: application/json" \
  -d "{\"Image\": {\"Bytes\": \"$(base64 -i ./database/db_images/jayvin.jpg)\"} }" \
  http://localhost:8000/api/predict
```

### Database Service Tests

```bash
# Check database health
curl http://localhost:5002/api/health

# Get a student by ID
curl http://localhost:5002/api/student?studentId=jayvin

# Add a new student
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"studentId": "newstudent", "name": "New Student", "email": "new@example.com", "photoReference": "newstudent.jpg"}' \
  http://localhost:5002/api/student
```

## Stopping the Services

```bash
# Stop all services but keep volumes
docker-compose down

# Stop services and remove volumes (complete cleanup)
docker-compose down -v
```