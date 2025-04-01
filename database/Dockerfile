# Stage 1: Base
FROM python:3.9-slim as base
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Make scripts executable
RUN chmod +x /app/entrypoint.sh

# Stage 2: Test Stage
FROM base as test
RUN pip install --no-cache-dir pytest
CMD ["python", "-m", "pytest", "--maxfail=1", "--disable-warnings", "-q"]

# Stage 3: Runtime
FROM base as runtime

# Set environment variables
ENV DATABASE_PATH=/app/students.db
ENV STUDENTS_JSON=/app/students.json
ENV IMAGES_DIR=/app/db_images
ENV IMAGES_OUTPUT_DIR=/app/images

# Create output directory
RUN mkdir -p /app/images

EXPOSE 5002
CMD ["/app/entrypoint.sh"]
