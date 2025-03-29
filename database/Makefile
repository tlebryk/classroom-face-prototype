.PHONY: test build run stop clean all test-curl shell test-from-container

# Default values - can be overridden at runtime
NETWORK ?= app-network
PORT ?= 5002
HOST_PORT ?= 5002
SERVICE_NAME ?= database

# Runs the tests in the test stage.
test:
	docker build --target test -t $(SERVICE_NAME)-test .
	docker run --rm $(SERVICE_NAME)-test

# Builds the production image.
build:
	docker build --target runtime -t $(SERVICE_NAME) .

# Runs the production container in detached mode using a network.
run:
	-docker network create $(NETWORK) 2>/dev/null || true
	docker run --init -d -p $(HOST_PORT):$(PORT) --name $(SERVICE_NAME) --network $(NETWORK) $(SERVICE_NAME)

# Stops and removes the running container.
stop:
	-docker stop $(SERVICE_NAME) || true
	-docker rm $(SERVICE_NAME) || true

# Clean up the container and the network.
clean: stop
	-docker network rm $(NETWORK) 2>/dev/null || true

# Stops previous containers, runs tests, builds the production image, and starts the container.
all: stop build run

# Use curl to test the running container endpoints from the host.
test-curl:
	@echo "Testing GET /api/student?studentId=stu123"
	curl -s http://localhost:$(HOST_PORT)/api/student?studentId=stu123
	@echo "\n\nTesting POST /api/student"
	curl -X POST http://localhost:$(HOST_PORT)/api/student \
	  -H "Content-Type: application/json" \
	  -d '{"studentId": "stu789", "name": "Bob Smith", "email": "bob@example.com", "photoReference": "ref2"}'
	@echo "\n\nTesting GET /api/student?studentId=stu789"
	curl -s http://localhost:$(HOST_PORT)/api/student?studentId=stu789
	@echo ""

# Test from another container (useful for debugging integration)
test-from-container:
	docker run --rm --network $(NETWORK) curlimages/curl:latest \
	  -X GET http://$(SERVICE_NAME):$(PORT)/api/student?studentId=stu123

# Opens an interactive shell inside a temporary container.
shell:
	docker run --rm -it $(SERVICE_NAME) /bin/bash
