import argparse
import base64
import logging
import os
import socket
import sys
import time
import traceback
from datetime import datetime

import cv2  # Requires: pip install opencv-python
import numpy as np
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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
        "ML_SERVICE_URL", "http://localhost:8000/api/predict"
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
        "ML_SERVICE_URL", "http://localhost:8000/api/predict"
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
        "STUDENT_DB_URL", "http://localhost:5002/api/student"
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


def process_capture(image_data, seat_id=None):
    logger.info("Starting image capture processing")

    try:
        logger.info("Calling ML service for face detection")
        ml_result = call_ml_service(image_data)
    except Exception as e:
        logger.error(f"ML service processing failed: {str(e)}")
        return {"error": str(e)}, 500

    # Check if a match was found and if the similarity is over 50%
    if not ml_result.get("match") or ml_result.get("similarity", 0) < 50:
        logger.warning("No face detected or low confidence in ML results")
        return {"error": "No face detected or low confidence"}, 400

    # Extract student info directly from the ML result
    predicted_student_id = ml_result.get("studentId", None)
    student_info = ml_result.get("studentInfo", {})
    similarity = (
        ml_result.get("similarity", 0) / 100
        if ml_result.get("similarity", 0) > 1
        else ml_result.get("similarity", 0)
    )

    logger.info(
        f"Face detected: Student ID = {predicted_student_id}, Similarity = {similarity}"
    )

    update_payload = {
        "studentId": predicted_student_id if predicted_student_id else None,
        "name": student_info.get("name", None),
        "seatId": seat_id,
        "confidence": similarity,
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
        "student_info": student_info,
        "frontend_update": update_payload,
        "frontend_response": frontend_response,
        "message": "Capture and update successful",
    }
    logger.info("Image capture processing completed successfully")
    return result, 200
def capture_image():
    """
    Capture an image from the webcam, enhance quality, and return a base64 string.
    """
    logger.info("Attempting to open webcam for image capture")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        logger.error("Cannot open webcam")
        return None
        
    # Try to set better camera parameters (may not work on all webcams)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 150)  # Increase brightness (0-255)
    cap.set(cv2.CAP_PROP_CONTRAST, 150)    # Increase contrast (0-255)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Auto exposure
    
    # Capture frame
    ret, frame = cap.read()
    cap.release()

    if not ret:
        logger.error("Failed to capture image from webcam")
        return None
    
    # Enhance image quality for better face detection
    enhanced_frame = enhance_image_quality(frame)
    
    # Save both original and enhanced images for comparison
    cv2.imwrite("captured_image_original.jpg", frame)
    cv2.imwrite("captured_image.jpg", enhanced_frame)
    print("Images saved as captured_image.jpg and captured_image_original.jpg")
    
    # Encode the enhanced image as JPEG
    ret, buffer = cv2.imencode(".jpg", enhanced_frame)
    if not ret:
        logger.error("Failed to encode captured image")
        return None
        
    jpg_bytes = buffer.tobytes()
    # Encode the bytes in base64 to safely include in JSON
    encoded_image = base64.b64encode(jpg_bytes).decode("utf-8")
    logger.info("Image captured, enhanced, and encoded successfully")
    return encoded_image

def enhance_image_quality(image):
    """
    Enhance image quality to improve face detection in low light conditions.
    """
    # Make a copy to avoid modifying the original
    enhanced = image.copy()
    
    # 1. Convert to LAB color space for better contrast enhancement
    if len(enhanced.shape) == 3:  # Color image
        lab = cv2.cvtColor(enhanced, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # 2. Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) to L channel
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        cl = clahe.apply(l)
        
        # 3. Merge channels back
        enhanced_lab = cv2.merge((cl, a, b))
        enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    else:  # Grayscale image
        # Apply CLAHE directly
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(enhanced)
    
    # 4. Additional brightness adjustment if needed
    # Calculate average brightness
    avg_brightness = np.mean(enhanced)
    
    # If image is still dark after CLAHE, boost brightness further
    if avg_brightness < 100:  # Adjust threshold based on testing
        # Create a brightness increase matrix
        brightness_increase = min(50, 120 - avg_brightness)  # Avoid excessive brightening
        enhanced = cv2.convertScaleAbs(enhanced, alpha=1.0, beta=brightness_increase)
    
    # 5. Optional: Slight sharpening for better facial features
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    enhanced = cv2.filter2D(enhanced, -1, kernel)
    
    # 6. Optional: Slight noise reduction
    enhanced = cv2.GaussianBlur(enhanced, (3, 3), 0)
    
    return enhanced

def main():
    parser = argparse.ArgumentParser(description="Run camera service")

    parser.add_argument(
        "-i",
        "--image_data",
        nargs="?",
        help="Base64 encoded image data to process (or capture from webcam if not provided)",
    )
    parser.add_argument(
        "-s",
        "--seat_id",
        help="Seat ID to associate with the captured student (or set via SEAT_ID environment variable)",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enable debug logging (default: info)",
    )
    args = parser.parse_args()

    logger.setLevel(logging.DEBUG if args.debug else logging.INFO)

    image_data = args.image_data
    seat_id = args.seat_id

    if not image_data:
        logger.info("No image data provided, capturing from webcam")
        image_data = capture_image()
        if image_data is None:
            logger.error("Image capture failed, exiting")
            sys.exit(1)

    if not seat_id:
        seat_id = os.environ.get("SEAT_ID", None)
        if not seat_id:
            logger.error("No seat ID provided, exiting")
            sys.exit(1)

    logger.info(
        f"Processing capture with image data (first 20 chars): {image_data[:20]}..."
    )
    result, status = process_capture(image_data, seat_id)
    logger.info(f"Process completed with status: {status}")
    logger.debug(f"Result: {result}")

    # Print results to stdout as well (for compatibility with existing code)
    print("Status:", status)
    print("Result:", result)

    logger.info("Camera service shutting down")
    sys.exit(status)


if __name__ == "__main__":
    main()
