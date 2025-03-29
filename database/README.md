# Classroom Facial Recognition System - Database Service

This service provides a lightweight REST API to interact with a SQLite database that stores student information. It is part of the prototype system to map student identities to seating positions in a classroom.

## Features

- **GET /api/student**: Retrieve student details by `studentId`
- **POST /api/student**: Add a new student record
- Initializes the database with a sample record (`stu123`)
- Built with Flask and SQLite

## Prerequisites

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- GNU Make

## Getting Started

### 1. Build, Test, and Run

Use the provided Makefile commands:

- **Run unit tests (inside the Docker container):**
  ```bash
  make test
  ```
Build the production image:

```bash

make build
```
Run the container in detached mode (listening on port 5000):

```bash

make run
```
2. Integration Testing with cURL
After running the container, you can use curl to test the endpoints:

GET an existing student:

```bash

curl -X
``` GET "http://localhost:5000/api/student?studentId=stu123"
POST a new student:

```bash

curl -X
 POST "http://localhost:5000/api/student" \
  -H "Content-Type: application/json" \
  -d '{"studentId": "stu789", "name": "Bob Smith", "email": "bob@example.com", "photoReference": "ref2"}'
```
Or run all integration tests using:

```bash

make test-curl
```

3. Stop the Service
To stop and remove the running container:

```bash
make stop
```

## TODO:
Add our real records to this database.
Optional:
    - Add table layout table.
    - Figure out student pictures