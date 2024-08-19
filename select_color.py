import cv2
import threading
from tkinter import *
import numpy as np
# Set up the main Tkinter window
frame = Tk()
frame.geometry('840x600')
hue = PhotoImage(file='mycode\hue.png')
# Initialize the Tkinter StringVars for the HSV limits
hl = StringVar(value='0')
sl = StringVar(value='50')
vl = StringVar(value='50')
hh = StringVar(value='180')
sh = StringVar(value='255')
vh = StringVar(value='255')

ch = StringVar(value='0')

# Open the camera
camera = cv2.VideoCapture(0)

# Function to handle the video capture and color detection
def process_video():
    while True:
        # Read the frame from the camera
        success, img = camera.read()
        if not success:
            continue

        # Convert the frame to HSV
        hsvc = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Get the HSV limits from the GUI (convert them from strings to integers)
        try:
            lowlimit = np.array([int(hl.get()), int(sl.get()), int(vl.get())])
            highlimit = np.array([int(hh.get()), int(sh.get()), int(vh.get())])
        except ValueError:
            # Handle the case where the GUI sliders have not been set correctly
            continue

        # Create a mask using the HSV limits
        mask = cv2.inRange(hsvc, lowlimit, highlimit)

        # Find contours in the mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw rectangles around detected objects
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 300:  # Filter out small contours
                x, y, w, h = cv2.boundingRect(contour)
                img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 255), 2)
                if ch.get() == "1":
                    break
                    

        # Display the image
        cv2.imshow('test', img)

        # Exit if 'ESC' key is pressed
        k= cv2.waitKey(1) 
        if k ==  ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
    frame.quit()
def print_values():
    lowlimit_values = [int(hl.get()), int(sl.get()), int(vl.get())]
    highlimit_values = [int(hh.get()), int(sh.get()), int(vh.get())]

    
    print("Low Limit values:  ", lowlimit_values)
    print("High Limit values: ", highlimit_values)

# Set up the GUI sliders for setting HSV limits
def setup_gui():
    label = Label(frame, image=hue)
    h_low = Scale(frame, orient=HORIZONTAL,length=1000,  from_=0, to=180, variable=hl, label="H Low")
    s_low = Scale(frame, orient=HORIZONTAL,length=1000,  from_=0, to=255, variable=sl, label="S Low")
    v_low = Scale(frame, orient=HORIZONTAL,length=1000,  from_=0, to=255, variable=vl, label="V Low")
    h_high = Scale(frame,orient=HORIZONTAL,length=1000,  from_=0, to=180, variable=hh, label="H High")
    s_high = Scale(frame,orient=HORIZONTAL,length=1000,  from_=0, to=255, variable=sh, label="S High")
    v_high = Scale(frame,orient=HORIZONTAL,length=1000,  from_=0, to=255, variable=vh, label="V High")
    chk = Checkbutton(frame, text="One Object", variable= ch, onvalue=1, offvalue=0)
    copy_button = Button(frame, text="Copy", command=print_values, height=2, width=50)
    # Pack the sliders into the Tkinter window
    label.pack()

    h_low.pack()
    s_low.pack()
    v_low.pack()
    h_high.pack()
    s_high.pack()
    v_high.pack()
    chk.pack()
    copy_button.place(x= 250, y=550)
    # Start the video processing in a separate thread
    threading.Thread(target=process_video, daemon=True).start()

    # Start the Tkinter main loop
    frame.mainloop()

# Run the GUI setup in the main thread
setup_gui()
