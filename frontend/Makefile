.PHONY: test build run stop clean all test-curl

# Default values - can be overridden at runtime
NETWORK ?= app-network
PORT ?= 3000
HOST_PORT ?= 3000
SERVICE_NAME ?= frontend

# Runs the tests in the tester stage.
test:
	docker build --target tester -t $(SERVICE_NAME)-test .
	docker run --rm $(SERVICE_NAME)-test

# Builds the production image.
build:
	docker build --target production -t $(SERVICE_NAME) .

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

# Runs tests, builds the production image, and starts the container.
all: stop build run

# Use curl to test the running container endpoints.
test-curl:
	@echo "Testing POST /api/classroom/update"
	curl -X POST http://localhost:$(HOST_PORT)/api/classroom/update \
	  -H "Content-Type: application/json" \
	  -d '{"studentId": "stu123", "name": "Alex Johnson", "seatId": "seat5", "confidence": 0.92, "lastSeen": "2025-03-28T12:34:56Z"}'
	@echo "\n\nTesting GET /api/classroom"
	curl http://localhost:$(HOST_PORT)/api/classroom?classroomId=default
	@echo ""


# Test from another container (useful for debugging integration)
test-from-container:
	docker run --rm --network $(NETWORK) curlimages/curl:latest \
	  -X POST http://$(SERVICE_NAME):$(PORT)/api/classroom/update \
	  -H "Content-Type: application/json" \
	  -d '{"studentId": "stu123", "name": "Andre Johnson", "seatId": "seat1", "confidence": 0.92, "lastSeen": "2025-03-28T12:34:56Z"}'