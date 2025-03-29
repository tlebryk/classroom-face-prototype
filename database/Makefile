.PHONY: test build run stop all test-curl

# Runs the tests in the test stage.
test:
	docker build --target test -t database-test .
	docker run --rm database-test

# Builds the production image.
build:
	docker build --target runtime -t database .

# Runs the production container in detached mode.
run:
	docker run --init -d -p 5000:5000 --name database database

# Stops and removes the running container.
stop:
	-docker stop database || true
	-docker rm database || true

# Runs tests, builds the production image, and starts the container.
all: test build run

# Use curl to test the running container endpoints.
test-curl:
	@echo "Testing GET /api/student?studentId=stu123"
	curl -s http://localhost:5000/api/student?studentId=stu123
	@echo "\n\nTesting POST /api/student"
	curl -X POST http://localhost:5000/api/student \
	  -H "Content-Type: application/json" \
	  -d '{"studentId": "stu789", "name": "Bob Smith", "email": "bob@example.com", "photoReference": "ref2"}'
	@echo "\n\nTesting GET /api/student?studentId=stu789"
	curl -s http://localhost:5000/api/student?studentId=stu789
	@echo ""
