.PHONY: all frontend database camera

# Build all services, with camera built last.
all: ml_service frontend database camera

ml_service:
	$(MAKE) -C ml_service all


# Build the frontend service.
frontend:
	$(MAKE) -C frontend all

# Build the database service.
database:
	$(MAKE) -C database all

# Build the camera service.
# Override the URLs so that the camera service reaches other services via their container names.
camera:
	$(MAKE) -C camera all \
	  ML_SERVICE_URL=http://ml-service:5001/api/predict \
	  STUDENT_DB_URL=http://database:5002/api/student \
	  FRONTEND_UI_URL=http://frontend:3000/api/classroom/update
