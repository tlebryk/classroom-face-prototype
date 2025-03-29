# Classroom Face Prototype

This project is a multi-service application that integrates a machine learning service, a frontend, a database, and a camera service for classroom face recognition.

## Services

- **ml_service**: Provides ML-based face detection/recognition (exposes HTTP endpoints on port 5001).
- **frontend**: Hosts the user interface and classroom updates (exposes HTTP endpoints on port 3000).
- **database**: Manages student data (exposes HTTP endpoints on port 5002).
- **camera**: A one-shot service that captures an image, processes it, and triggers updates in the other services.

## Prerequisites

- [Docker](https://www.docker.com/) installed and running.
- Basic familiarity with Docker and Makefiles.

## Getting Started

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
2. Build and run all services:

From the repository root, run:

```bash
make all
```
or 
```bash 
docker-compose run camera
```
Either command will: Build and run the  frontend, database, ml service and finally the "camera" service. The camera service then hits the frontend, database, and ml service with requests to fulfill the pipeline.  

3.  Running individual services:

You can also build or run services individually:

- ml_service: make ml_service
- frontend: make frontend
- database: make database
- camera: make camera