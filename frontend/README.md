# Frontend Service for Classroom Facial Recognition

This service is a lightweight mock frontend for a classroom facial recognition system. It receives classroom updates and serves a static classroom layout via two endpoints.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Make](https://www.gnu.org/software/make/)

## File Structure

- **main.js**: Express application exposing the API endpoints.
- **Dockerfile**: Multi-stage build file with:
  - **tester** stage: Runs integration tests.
  - **production** stage: Builds the runnable app image.
- **Makefile**: Contains useful commands to test, build, run, and stop the service.

## API Endpoints

- **POST /api/classroom/update**  
  Receives classroom updates (JSON payload).  
- **GET /api/classroom**  
  Returns a static classroom layout.

## Using the Makefile

### Run Integration Tests

Build the tester stage image and run tests:
```bash
make test
```

### Build the Production Image

Build the production image from the Dockerfile:
```bash
make build
```

### Run the Production Container

Start the container in detached mode (listening on port 3000):
```bash
make run
```

### Test Endpoints with cURL

Once the container is running, send sample requests:
```bash
make test-curl
```

This target sends:
- A POST request to `/api/classroom/update`
- A GET request to `/api/classroom?classroomId=default`

### Stop and Remove the Container

Clean up the running container:
```bash
make stop
```

### All-in-One Command

Run tests, build the image, and start the container:
```bash
make all
```

## Summary of Commands

- **make test**: Runs integration tests in the tester stage.
- **make build**: Builds the production Docker image.
- **make run**: Runs the production container.
- **make test-curl**: Tests endpoints with curl.
- **make stop**: Stops and removes the container.
- **make all**: Runs tests, builds, and starts the container.

## TODO:
- fill out real UI and rendering features