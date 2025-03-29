# Classroom Facial Recognition System

## Overview

This prototype demonstrates how facial recognition can be used to automatically map student identities to their seating positions in a classroom. The system captures student images via a webcam, sends them to an ML service for facial recognition, cleans and enriches the data using a student database, and posts the processed information to a frontend service for rendering.

## Features

- **Camera Endpoint:** Manually trigger image capture via CLI.
- **Facial Recognition Integration:** Send images to an ML service and filter predictions based on confidence.
- **Student Data Enrichment:** Retrieve additional student details from a SQLite database.
- **Frontend Update:** Post processed student data for classroom rendering.
- **Dockerized Environment:** Multi-stage Docker builds for testing and runtime.
- **Automated Testing:** Unit tests implemented using pytest.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed.
- (Optional) Python 3.9+ for local development and testing.

## Getting Started

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
Set Environment Variables:

The following environment variables are used by the service (defaults provided in the Makefile):

ML_SERVICE_URL (default: http://localhost:5001/api/predict)

STUDENT_DB_URL (default: http://localhost:5000/api/student)

FRONTEND_UI_URL (default: http://localhost:3000/api/classroom/update)

Run this container (will need to have other services running to work)
```bash
make all
```

Run Tests: Execute the unit tests with:

```bash
make test
```
Build the Docker Image: Build the production image using:

```bash
make build
```
Run the Service: Start the service as a one-shot script by running:

```bash
make run
```
Interactive Shell (Optional): Open a temporary container shell to debug:

```bash
make shell
```

## Project Structure

app.py: Main Flask application that handles the student database endpoints and image processing workflow.

Makefile: Contains commands for testing, building, running, and managing the Docker containers.

Dockerfile: Multi-stage build (base, test, and runtime stages) for streamlined deployment.

tests/test_app.py: Pytest-based unit tests covering ML service integration, student DB queries, frontend updates, and overall capture processing.

## TODO
- add integration with device camera. 
- have real image serialization to send to ml-service