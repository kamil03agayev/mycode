import cv2
import time
import numpy as np
# from PIL import Image
# import tkinter as tk

# window = tk.Tk()
# window.geometry('500x500')
# tolerance_field = tk.Entry(window)

# xmin, ymin, xmax, ymax = 0, 0, 0, 0
# line_color = (0, 255, 0)
colors =  [[5,236,201],  #redcolor
           [87,255,38], #greencolor
           [123,149,82]]  #violet color
draw_color = [0, 255, 0]
object_color = draw_color
ptime, ctime = 0, 0
color_tolerance = 15
lowl = 130
highl = 250
camera = cv2.VideoCapture(0)

def detect_color(image, color, s):
    hsvc = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    if s == 0:
        lowlimit1 = np.array([0, 150, 150])
        highlimit1 = np.array([5, 255, 255])
        lowlimit2 = np.array([175, 100, 100])
        highlimit2 = np.array([180, 255, 255])

        red_mask1 = cv2.inRange(hsvc, lowlimit1, highlimit1)
        red_mask2 = cv2.inRange(hsvc, lowlimit2, highlimit2)
        red_mask = cv2.bitwise_or(red_mask1, red_mask2)
        return red_mask
    elif s == 1:
        lowlimit1 = np.array([25, 52, 72])
        highlimit1 = np.array([102, 255, 255])
        green_mask = cv2.inRange(hsvc, lowlimit1, highlimit1)
        return green_mask
    elif s == 2:
        lowlimit1 = np.array([0, 100, 150])
        highlimit1 = np.array([5, 255, 255])
        violet_mask = cv2.inRange(hsvc, lowlimit1, highlimit1)
        return violet_mask
    # else:
    #     hsvc = np.uint8([[color]])
        
    #     lowlimit = hsvc[0][0][0] - color_tolerance, lowl, lowl
    #     highlimit = hsvc[0][0][0] + color_tolerance, highl, highl
        
    #     lowlimit = np.array(lowlimit, dtype=np.uint8)
    #     highlimit = np.array(highlimit, dtype=np.uint8)
        
    #     hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #     mask = cv2.inRange(hsv_img, lowlimit, highlimit)
    #     return mask
    # return lowlimit, highlimit

def draw_elements(img, object_color):
    global cx, cy
    height, width, _ = img.shape

    img = cv2.line(img, (int(width/3), 0), (int(width/3), height), draw_color, thickness = 1)
    img = cv2.line(img, (int(width/3*2), 0), (int(width/3*2), height), draw_color, thickness = 1)


    return img

while True:
    success, img = camera.read()
    # width, height, c = img.shape
    height, width, _ = img.shape


    mask = detect_color(image=img, color=colors[0], s = 0)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) 
    if hierarchy is not None and len(contours)> 0:
        object_color = [0, 0, 255]
        color_name = 'red'
        # print("I found red!!!")
    else:
        mask = detect_color(image=img, color=colors[1], s = 1)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if hierarchy is not None and len(contours)> 0:   
            object_color = [0, 255, 0]
            color_name = 'green'
            # print("I found green!!!")
        else:
            mask = detect_color(image=img, color=colors[2], s = 2)
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if hierarchy is not None and len(contours) > 0:  
                object_color = [255, 0, 255]
                color_name = 'violet'
                # print("I found violet!!!")
    
    for pic, contour in enumerate(contours): 
        area = cv2.contourArea(contour) 
        # print("--------------------------------")
        # print(len(contour))
        # print("--------------------------------")

        if(area > 300): 
            x, y, w, h = cv2.boundingRect(contour) 
            img = cv2.rectangle(img, (x, y),  (x + w, y + h), draw_color, 2) 
            cx, cy = int(x+w/2), int(y+h/2)
            img = cv2.line(img, (cx, 0), (cx, height), draw_color, thickness = 2)  
            img = cv2.rectangle(img, (width-40, 20), (width - 20, 80), object_color, thickness = -1)
            if cx > int(width/3) and cx < int(width/3*2) and color_name != 'violet':
                print("Its good!!!")
            elif cx < int(width/3) and color_name == 'green':
                print('Left side')
            elif cx > int(width/3*2) and color_name == 'green':
                print('Right side')  
            elif cx < int(width/3) and color_name == 'red':
                print('Right side')
            elif cx > int(width/3*2) and color_name == 'red':
                print('Left side')   
            # print(f'Detected color: {color_name}')

            break  
  
    # img = cv2.rectangle(img, (int(round(xmin)), int(round(ymin))), (int(round(xmax)), int(round(ymax))), (255, 0, 0), 1)
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv2.putText(img, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, draw_color, 2)
    
    img = draw_elements(img, object_color)
    
    cv2.imshow('test',mask)
    cv2.imshow('IMAGE', img)
    k= cv2.waitKey(1) 
    if k ==  ord('q'):
        break
    
