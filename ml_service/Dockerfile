# Stage 1: Base
FROM python:3.9-slim as base
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Stage 2: Tester
FROM base as tester
RUN pip install --no-cache-dir pytest
CMD ["python", "-m", "pytest", "--maxfail=1", "--disable-warnings", "-q"]

# Stage 3: Production
FROM base as production
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
