.PHONY: test build run stop all test-curl

# Runs the tests in the tester stage.
test:
	docker build --target tester -t ml-service-test .
	docker run --rm ml-service-test

# Builds the production image.
build:
	docker build --target production -t ml-service .

# Runs the production container in detached mode.
run:
	docker run --init -d -p 5001:5001 --name ml-service --network app-network ml-service

# Stops and removes the running container.
stop:
	-docker stop ml-service || true
	-docker rm ml-service || true

# Runs tests, builds the production image, and starts the container.
all: stop test build run

# Use curl to test the running container endpoint.
test-curl:
	@echo "Testing POST /api/predict"
	curl -X POST http://ml-service:5001/api/predict \
	  -H "Content-Type: application/json" \
	  -d '{"CollectionId": "student-gallery", "Image": {"Bytes": "dummy"}, "MaxFaces": 1, "FaceMatchThreshold": 80}'
	@echo ""
