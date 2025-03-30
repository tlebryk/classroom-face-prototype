.PHONY: test build run stop all test-curl shell

# Default values - can be overridden at runtime
NETWORK ?= app-network
SERVICE_NAME ?= camera
HOST_PORT ?= 5000
CONTAINER_PORT ?= 5000

# Environment variables for the real app
ML_SERVICE_URL ?= http://ml-service:5001/api/predict
STUDENT_DB_URL ?= http://database:5002/api/student
FRONTEND_UI_URL ?= http://frontend:3000/api/classroom/update

# Runs the tests in the test stage.
test:
	docker build --target test -t $(SERVICE_NAME)-test .
	docker run --rm $(SERVICE_NAME)-test

# Builds the production image.
build:
	docker build --target runtime -t $(SERVICE_NAME) .

# Runs the production container as a one-shot script.
# Passes the necessary environment variables.
run:
	docker run --rm --name $(SERVICE_NAME) \
	  -e ML_SERVICE_URL=$(ML_SERVICE_URL) \
	  -e STUDENT_DB_URL=$(STUDENT_DB_URL) \
	  -e FRONTEND_UI_URL=$(FRONTEND_UI_URL) \
	  --network $(NETWORK) \
	  $(SERVICE_NAME)

clean: stop
	-docker network rm $(NETWORK) 2>/dev/null || true

# Stops and removes the running container.
stop:
	-docker stop $(SERVICE_NAME) || true
	-docker rm $(SERVICE_NAME) || true

# Stops previous containers, runs tests, builds the production image, and runs the service.
all: stop build run

# Since the camera service does not expose HTTP endpoints, this target is not applicable.
test-curl:
	@echo "Camera service is a one-shot script. Use 'make run' to trigger the capture process."

# Opens an interactive shell inside a temporary container.
shell:
	docker run --rm -it -v "$(shell pwd):/app" camera /bin/bash
