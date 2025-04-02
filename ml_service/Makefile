.PHONY: test build run run-networked stop clean all test-curl integration-test

# Default values - can be overridden at runtime
NETWORK ?= app-network
PORT ?= 8000
HOST_PORT ?= 8000
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
	docker run --init -d -p 8000:8000 \
	--name ml-service \
	-e DATABASE_URL=http://database:5002 \
	-e REFERENCE_FACES_DIR=/app/reference_faces \
	-v database-images:/app/reference_faces \
	--network $(NETWORK) \
	ml-service

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
	@base64 -i $(abspath ../database/db_images/jayvin.jpg) > /tmp/encoded_image.txt
	@curl -X POST http://localhost:$(HOST_PORT)/api/predict \
	  -H "Content-Type: application/json" \
	  -d "{\"Image\": {\"Bytes\": \"$$(cat /tmp/encoded_image.txt)\"} }"
	@rm -f /tmp/encoded_image.txt
	@echo ""
# Test from another container (useful for debugging integration)
test-from-container:
	docker run --rm --network $(NETWORK) curlimages/curl:latest \
	  -X POST http://$(SERVICE_NAME):$(PORT)/api/predict \
	  -H "Content-Type: application/json" \
	  -d "{"Image": {"Bytes": "$(base64 -i ./database/db_images/jayvin.jpg)"} }" 

camera:
	docker run --rm --network $(NETWORK) \
	  -e ML_SERVICE_URL=http://$(SERVICE_NAME):$(PORT)/api/predict \
	  camera 

shell:
	docker run --rm -it -v "$(shell pwd):/app" $(SERVICE_NAME) /bin/bash
