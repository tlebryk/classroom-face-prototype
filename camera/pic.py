import cv2

# Open a connection to the webcam (0 is usually the default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Read one frame from the webcam
ret, frame = cap.read()

if not ret:
    print("Can't receive frame (stream end?). Exiting ...")
    exit()

# Display the captured frame in a window
cv2.imshow("Captured Image", frame)

# Save the captured image to a file
cv2.imwrite("captured_image.jpg", frame)
print("Image saved as captured_image.jpg")

# Wait for any key to be pressed
cv2.waitKey(0)

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
