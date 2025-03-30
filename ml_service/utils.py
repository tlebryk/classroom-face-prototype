import base64
import cv2
import numpy as np
import matplotlib.pyplot as plt


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
