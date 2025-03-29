import os
import requests
from datetime import datetime
import sys
import logging
import traceback
import socket

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


def log_network_info():
    """Log network configuration to help with debugging"""
    logger.info(f"Current hostname: {socket.gethostname()}")
    try:
        # Try to resolve ml-service hostname (works if using Docker network)
        logger.info(
            f"Trying to resolve 'ml-service': {socket.gethostbyname('ml-service')}"
        )
    except socket.gaierror:
        logger.warning("Could not resolve 'ml-service' hostname")

    # Log environment variables
    ml_service_url = os.environ.get(
        "ML_SERVICE_URL", "http://localhost:5001/api/predict"
    )
    logger.info(f"ML_SERVICE_URL = {ml_service_url}")

    # Try a basic connection to the ML service
    try:
        host = ml_service_url.split("://")[1].split("/")[0]  # Extract host:port
        if ":" in host:
            host, port = host.split(":")
            port = int(port)
        else:
            port = 80 if ml_service_url.startswith("http://") else 443

        logger.info(f"Testing basic socket connection to {host}:{port}")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        result = s.connect_ex((host, port))
        if result == 0:
            logger.info(f"Socket connection to {host}:{port} succeeded")
        else:
            logger.error(
                f"Socket connection to {host}:{port} failed with error code {result}"
            )
        s.close()
    except Exception as e:
        logger.error(f"Socket test failed: {str(e)}")
        logger.debug(traceback.format_exc())


def call_ml_service(image_data):
    ML_SERVICE_URL = os.environ.get(
        "ML_SERVICE_URL", "http://localhost:5001/api/predict"
    )
    logger.info(f"Calling ML service at: {ML_SERVICE_URL}")

    ml_payload = {
        "CollectionId": "student-gallery",
        "Image": {"Bytes": image_data},
        "MaxFaces": 1,
        "FaceMatchThreshold": 80,
    }

    try:
        logger.debug(f"Sending POST request to ML service with payload: {ml_payload}")
        response = requests.post(ML_SERVICE_URL, json=ml_payload)
        logger.info(f"ML service response status: {response.status_code}")

        if response.status_code != 200:
            logger.error(f"ML Service error: {response.text}")
            raise Exception(f"ML Service error: {response.text}")

        result = response.json()
        logger.debug(f"ML service response: {result}")
        return result

    except requests.exceptions.ConnectionError as e:
        logger.error(f"Connection error to ML service: {str(e)}")
        logger.debug(traceback.format_exc())
        raise
    except Exception as e:
        logger.error(f"Unexpected error in call_ml_service: {str(e)}")
        logger.debug(traceback.format_exc())
        raise


import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def create_retry_session(retries=5, backoff_factor=0.5):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def query_student_db(student_id):
    STUDENT_DB_URL = os.environ.get(
        "STUDENT_DB_URL", "http://localhost:5000/api/student"
    )
    logger.info(f"Querying student DB at: {STUDENT_DB_URL} for student: {student_id}")

    # Use session with retries
    session = create_retry_session()

    try:
        response = session.get(STUDENT_DB_URL, params={"studentId": student_id})
        logger.info(f"Student DB response status: {response.status_code}")

        if response.status_code != 200:
            logger.error(f"Student DB error: {response.text}")
            raise Exception(f"Student DB error: {response.text}")

        result = response.json()
        logger.debug(f"Student DB response: {result}")
        return result

    except Exception as e:
        logger.error(f"Error in query_student_db: {str(e)}")
        logger.debug(traceback.format_exc())
        raise


def update_frontend(update_payload):
    FRONTEND_UI_URL = os.environ.get(
        "FRONTEND_UI_URL", "http://localhost:3000/api/classroom/update"
    )
    logger.info(f"Updating frontend at: {FRONTEND_UI_URL}")

    try:
        response = requests.post(FRONTEND_UI_URL, json=update_payload)
        logger.info(f"Frontend response status: {response.status_code}")

        if response.status_code != 200:
            logger.error(f"Frontend UI error: {response.text}")
            raise Exception(f"Frontend UI error: {response.text}")

        result = response.json()
        logger.debug(f"Frontend response: {result}")
        return result

    except Exception as e:
        logger.error(f"Error in update_frontend: {str(e)}")
        logger.debug(traceback.format_exc())
        raise


def process_capture(image_data):
    logger.info("Starting image capture processing")

    try:
        logger.info("Calling ML service for face detection")
        ml_result = call_ml_service(image_data)
    except Exception as e:
        logger.error(f"ML service processing failed: {str(e)}")
        return {"error": str(e)}, 500

    if not ml_result.get("FaceMatches"):
        logger.warning("No face detected or low confidence in ML results")
        return {"error": "No face detected or low confidence"}, 400

    face_match = ml_result["FaceMatches"][0]
    predicted_student_id = face_match["Face"].get("ExternalImageId")
    confidence = face_match["Face"].get("Confidence")
    logger.info(
        f"Face detected: Student ID = {predicted_student_id}, Confidence = {confidence}"
    )

    try:
        logger.info("Querying student database for student details")
        student_data = query_student_db(predicted_student_id)
    except Exception as e:
        logger.error(f"Student DB query failed: {str(e)}")
        return {"error": str(e)}, 500

    # For simplicity, assign a static seat.
    seat_id = "seat5"
    update_payload = {
        "studentId": predicted_student_id,
        "name": student_data.get("name", ""),
        "seatId": seat_id,
        "confidence": confidence / 100 if confidence > 1 else confidence,
        "lastSeen": datetime.utcnow().isoformat() + "Z",
    }
    logger.info(f"Prepared frontend update payload: {update_payload}")

    try:
        logger.info("Sending update to frontend UI")
        frontend_response = update_frontend(update_payload)
    except Exception as e:
        logger.error(f"Frontend update failed: {str(e)}")
        return {"error": str(e)}, 500

    result = {
        "ml_result": ml_result,
        "student_data": student_data,
        "frontend_update": update_payload,
        "frontend_response": frontend_response,
        "message": "Capture and update successful",
    }
    logger.info("Image capture processing completed successfully")
    return result, 200


def main():
    logger.info("Camera service starting")

    # Log network configuration for debugging
    log_network_info()

    # Optionally, you can pass an image as the first argument. Default is "dummy".
    image_data = sys.argv[1] if len(sys.argv) > 1 else "dummy"
    logger.info(f"Processing capture with image data: {image_data[:20]}...")

    result, status = process_capture(image_data)
    logger.info(f"Process completed with status: {status}")
    logger.debug(f"Result: {result}")

    # Print results to stdout as well (for compatibility with existing code)
    print("Status:", status)
    print("Result:", result)

    logger.info("Camera service shutting down")
    sys.exit(status)


if __name__ == "__main__":
    main()
