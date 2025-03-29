.PHONY: test build run stop all test-curl shell

# Variables
IMAGE_NAME=camera
CONTAINER_NAME=camera
HOST_PORT=5000
CONTAINER_PORT=5000

# Runs the tests in the test stage.
test:
	docker build --target test -t $(IMAGE_NAME)-test .
	docker run --rm $(IMAGE_NAME)-test

# Builds the production image.
build:
	docker build --target runtime -t $(IMAGE_NAME) .

# Runs the production container (one-shot script).
# Since this service runs as a one-shot script, we run it without -d.
run:
	docker run --init --name $(CONTAINER_NAME) $(IMAGE_NAME)

# Stops and removes the running container.
stop:
	-docker stop $(CONTAINER_NAME) || true
	-docker rm $(CONTAINER_NAME) || true

# Stops previous containers, runs tests, builds the production image, and starts the container.
all: stop test build run

# Since the camera service does not expose HTTP endpoints, we note that test-curl is not applicable.
test-curl:
	@echo "Camera service is a one-shot script. Use 'make run' to trigger the capture process."

# Opens an interactive shell inside a temporary container.
shell:
	docker run --rm -it $(IMAGE_NAME) /bin/bash
