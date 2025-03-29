.PHONY: test build run run-networked stop clean all test-curl integration-test

# Default values - can be overridden at runtime
NETWORK ?= app-network
PORT ?= 5001
HOST_PORT ?= 5001
SERVICE_NAME ?= ml-service

# Runs the tests in the tester stage.
test:
	docker build --target tester -t $(SERVICE_NAME)-test .
	docker run --rm $(SERVICE_NAME)-test

# Builds the production image.
build:
	docker build --target production -t $(SERVICE_NAME) .

# Runs the production container in detached mode (localhost only).
run-local:
	docker run --init -d -p $(HOST_PORT):$(PORT) --name $(SERVICE_NAME) $(SERVICE_NAME)

# Runs the production container in a network (for integration testing).
run:
	-docker network create $(NETWORK) 2>/dev/null || true
	docker run --init -d -p $(HOST_PORT):$(PORT) --name $(SERVICE_NAME) --network $(NETWORK) $(SERVICE_NAME)

# Stops and removes the running container.
stop:
	-docker stop $(SERVICE_NAME) || true
	-docker rm $(SERVICE_NAME) || true

# Clean everything (containers and network)
clean: stop
	-docker network rm $(NETWORK) 2>/dev/null || true

# Runs tests, builds the production image, and starts the container.
all: stop build run


# Use curl to test the running container endpoint from the host.
test-curl:
	@echo "Testing POST /api/predict"
	curl -X POST http://localhost:$(HOST_PORT)/api/predict \
	  -H "Content-Type: application/json" \
	  -d '{"CollectionId": "student-gallery", "Image": {"Bytes": "dummy"}, "MaxFaces": 1, "FaceMatchThreshold": 80}'
	@echo ""

# Test from another container (useful for debugging integration)
test-from-container:
	docker run --rm --network $(NETWORK) curlimages/curl:latest \
	  -X POST http://$(SERVICE_NAME):$(PORT)/api/predict \
	  -H "Content-Type: application/json" \
	  -d '{"CollectionId": "student-gallery", "Image": {"Bytes": "dummy"}, "MaxFaces": 1, "FaceMatchThreshold": 80}'

camera:
	docker run --rm --network $(NETWORK) \
	  -e ML_SERVICE_URL=http://$(SERVICE_NAME):$(PORT)/api/predict \
	  camera 