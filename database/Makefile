.PHONY: test build run stop all test-curl shell

# Variables
IMAGE_NAME=database
CONTAINER_NAME=database
HOST_PORT=5002
CONTAINER_PORT=5002

# Runs the tests in the test stage.
test:
	docker build --target test -t $(IMAGE_NAME)-test .
	docker run --rm $(IMAGE_NAME)-test

# Builds the production image.
build:
	docker build --target runtime -t $(IMAGE_NAME) .

# Runs the production container in detached mode.
run:
	docker run --init -d -p $(HOST_PORT):$(CONTAINER_PORT) --name $(CONTAINER_NAME) $(IMAGE_NAME)

# Stops and removes the running container.
stop:
	-docker stop $(CONTAINER_NAME) || true
	-docker rm $(CONTAINER_NAME) || true

# Stops previous images, runs tests, builds the production image, and starts the container.
all: stop test build run

# Use curl to test the running container endpoints.
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

# Opens an interactive shell inside a temporary container.
shell:
	docker run --rm -it $(IMAGE_NAME) /bin/bash
