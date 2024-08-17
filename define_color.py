import cv2
import os
# print
# Open a connection to the camera
camera = cv2.VideoCapture(1)  # Use 0 for the default camera, or replace with the appropriate index

if not camera.isOpened():
    print("Error: Camera not opened.")
    exit()

while True:
    # Capture frame-by-frame
    success, frame = camera.read()
    frame = cv2.flip(frame, 1)
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    if not success:
        print("Error: Failed to capture image.")
        break

    # Get frame dimensions
    height, width, _ = frame.shape

    # Calculate the center coordinates
    center_x = width // 2
    center_y = height // 2

    # Get the BGR color of the center pixel
    color = img[center_y, center_x]  # OpenCV uses (y, x) for indexing
    b, g, r = color  # Extract BGR values


    # Optional: Display the frame with a circle at the center pixel
    frame_with_circle = frame.copy()
    cv2.circle(frame_with_circle, (center_x, center_y), 5, (0, 255, 0), -1)  # Draw a green circle
    cv2.imshow('Frame with Center Pixel', frame_with_circle)

    # Exit the loop if 'q' is pressed

    print(f"Center pixel color - [{b},{g},{r}]")
    os.system('cls')
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
camera.release()
cv2.destroyAllWindows()
