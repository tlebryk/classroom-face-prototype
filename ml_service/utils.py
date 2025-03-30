import base64
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import logging


def display_decoded_image(encoded_image):
    """
    Decode the base64 image, convert it to a format OpenCV can work with,
    and display it briefly using matplotlib.
    """
    try:
        # Decode the base64 string to bytes
        img_bytes = base64.b64decode(encoded_image)
        # Convert bytes to a numpy array
        nparr = np.frombuffer(img_bytes, np.uint8)
        # Decode the image from the numpy array
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            print("Failed to decode image.")
            return
        # Convert from BGR to RGB for display
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Display the image briefly
        plt.imshow(img_rgb)
        plt.title("Received Image")
        plt.axis("off")
        plt.show(block=False)
        plt.pause(1)  # Display for 1 second
        plt.close()
    except Exception as e:
        print(f"Error decoding image: {e}")


def save_decoded_image(encoded_image):
    """
    Decode the base64 image, convert it to an OpenCV image, and save it to a file.
    The output directory is specified by the IMAGE_OUTPUT_DIR environment variable,
    defaulting to /tmp if not set.
    """
    try:
        # Decode the base64 string to bytes
        img_bytes = base64.b64decode(encoded_image)
        # Convert bytes to a numpy array
        nparr = np.frombuffer(img_bytes, np.uint8)
        # Decode the image from the numpy array
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            logging.error("Failed to decode image.")
            return None

        # Determine the output directory and filename
        output_dir = os.environ.get("IMAGE_OUTPUT_DIR", "/tmp")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "decoded_image.jpg")

        # Save the image to the file
        success = cv2.imwrite(output_path, img)
        if success:
            logging.info(f"Image successfully saved to {output_path}")
            return output_path
        else:
            logging.error("Failed to save image.")
            return None
    except Exception as e:
        logging.error(f"Error decoding and saving image: {e}")
        return None
