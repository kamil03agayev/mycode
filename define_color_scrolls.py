import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
# print
# Global variables for HSV limits
lower_h = 0
lower_s = 0
lower_v = 0
upper_h = 179
upper_s = 255
upper_v = 255

# Initialize video capture
cap = cv2.VideoCapture(0)  # Use 0 for the default webcam

def update_image():
    global cap, lower_h, lower_s, lower_v, upper_h, upper_s, upper_v

    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        return

    # Convert the image from BGR to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define the HSV range
    lower_bound = np.array([lower_h, lower_s, lower_v])
    upper_bound = np.array([upper_h, upper_s, upper_v])
    
    # Create a mask and apply it
    mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    # Convert the result to a format suitable for Tkinter
    result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    result_image = Image.fromarray(result_rgb)
    result_image = ImageTk.PhotoImage(result_image)
    
    # Update the image on the Tkinter label
    result_label.config(image=result_image)
    result_label.image = result_image

    # Schedule the next frame update
    root.after(10, update_image)  # Update every 10 ms

# Update the HSV lower and upper limits based on slider values
def update_hsv(val):
    global lower_h, lower_s, lower_v, upper_h, upper_s, upper_v
    lower_h = hue_lower_slider.get()
    lower_s = saturation_lower_slider.get()
    lower_v = value_lower_slider.get()
    upper_h = hue_upper_slider.get()
    upper_s = saturation_upper_slider.get()
    upper_v = value_upper_slider.get()
    # Update the image with the new HSV values
    update_image()

# Create the main application window
root = tk.Tk()
root.title("HSV Color Detection")

# Create sliders for HSV limits
tk.Label(root, text="Hue Lower").pack()
hue_lower_slider = tk.Scale(root, from_=0, to_=179, orient='horizontal', command=update_hsv)
hue_lower_slider.pack()

tk.Label(root, text="Saturation Lower").pack()
saturation_lower_slider = tk.Scale(root, from_=0, to_=255, orient='horizontal', command=update_hsv)
saturation_lower_slider.pack()

tk.Label(root, text="Value Lower").pack()
value_lower_slider = tk.Scale(root, from_=0, to_=255, orient='horizontal', command=update_hsv)
value_lower_slider.pack()

tk.Label(root, text="Hue Upper").pack()
hue_upper_slider = tk.Scale(root, from_=0, to_=179, orient='horizontal', command=update_hsv)
hue_upper_slider.pack()

tk.Label(root, text="Saturation Upper").pack()
saturation_upper_slider = tk.Scale(root, from_=0, to_=255, orient='horizontal', command=update_hsv)
saturation_upper_slider.pack()

tk.Label(root, text="Value Upper").pack()
value_upper_slider = tk.Scale(root, from_=0, to_=255, orient='horizontal', command=update_hsv)
value_upper_slider.pack()

# Label to display the processed image
result_label = tk.Label(root)
result_label.pack()

# Start the image update loop
update_image()

# Run the application
root.mainloop()

# Release the video capture object when the application is closed
cap.release()
cv2.destroyAllWindows()
