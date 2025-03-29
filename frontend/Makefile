.PHONY: test build run stop all test-curl

# Runs the tests in the tester stage.
test:
	docker build --target tester -t frontend-test .
	docker run --rm frontend-test

# Builds the production image.
build:
	docker build --target production -t frontend .

# Runs the production container in detached mode.
run:
	docker run --init -d -p 3000:3000 --name frontend frontend

# Stops and removes the running container.
stop:
	-docker stop frontend || true
	-docker rm frontend || true

# Runs tests, builds the production image, and starts the container.
all: test build run

# Use curl to test the running container endpoints.
test-curl:
	@echo "Testing POST /api/classroom/update"
	curl -X POST http://localhost:3000/api/classroom/update \
	  -H "Content-Type: application/json" \
	  -d '{"studentId": "stu123", "name": "Alice Johnson", "seatId": "seat5", "confidence": 0.92, "lastSeen": "2025-03-28T12:34:56Z"}'
	@echo "\n\nTesting GET /api/classroom"
	curl http://localhost:3000/api/classroom?classroomId=default
	@echo ""
