# Stage 1: Base
FROM python:3.11-slim as base

RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create reference faces directory
# RUN mkdir -p reference_faces

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Stage 2: Tester
FROM base as tester
RUN pip install --no-cache-dir pytest
CMD ["python", "-m", "pytest", "--maxfail=1", "--disable-warnings", "-q"]

# Stage 3: Production
FROM base as production

ENV REFERENCE_FACES_DIR="/app/reference_faces"
ENV SIMILARITY_THRESHOLD=0.4 
ENV IMAGE_OUTPUT_DIR="/app/output"

# Create output directory for saved images
RUN mkdir -p /app/output

EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
