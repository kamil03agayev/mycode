import cv2
import time
import numpy as np

draw_color = [0, 255, 0]
object_color = draw_color
ptime, ctime = 0, 0
color_tolerance = 15
lowl = 130
highl = 250
lines_distance = 250
camera = cv2.VideoCapture(0)
crop = 0

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
        lowlimit1 = np.array([45, 70, 70])
        highlimit1 = np.array([90, 255, 255])
        green_mask = cv2.inRange(hsvc, lowlimit1, highlimit1)
        return green_mask
    elif s == 2:
        lowlimit1 = np.array([110, 50, 50])
        highlimit1 = np.array([140, 255, 255])
        violet_mask = cv2.inRange(hsvc, lowlimit1, highlimit1)
        return violet_mask
    

def draw_elements(img, object_color):
    global cx, cy
    height, width, _ = img.shape

    img = cv2.line(img, (int(lines_distance), 0), (int(lines_distance), height), draw_color, thickness = 1)
    img = cv2.line(img, (int(width-lines_distance), 0), (int(width-lines_distance), height), draw_color, thickness = 1)

    return img

while True:
    success, img = camera.read()
    
    height, width, _ = img.shape
    img = img[:, crop:width - crop]

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
        # print(len(contour))

        if(area > 300): 
            x, y, w, h = cv2.boundingRect(contour) 
            img = cv2.rectangle(img, (x, y),  (x + w, y + h), draw_color, 2) 
            cx, cy = int(x+w/2), int(y+h/2)
            img = cv2.line(img, (cx, 0), (cx, height), draw_color, thickness = 2)  
            img = cv2.rectangle(img, (width-40, 20), (width - 20, 80), object_color, thickness = -1)
            if cx > int(lines_distance) and cx < int(width-lines_distance) and color_name != 'violet':
                print("Its good!!!")
            elif cx < int(lines_distance) and color_name == 'green':
                print('Left side')
            elif cx > int(width-lines_distance) and color_name == 'green':
                print('Right side')  
            elif cx < int(lines_distance) and color_name == 'red':
                print('Right side')
            elif cx > int(width-lines_distance) and color_name == 'red':
                print('Left side')   
            # print(f'Detected color: {color_name}')
            break  
  
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv2.putText(img, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, draw_color, 2)
    
    img = draw_elements(img, object_color)
    
    cv2.imshow('mask',mask)
    cv2.imshow('Test', img)
    k= cv2.waitKey(1) 
    if k ==  ord('q'):
        break
    
camera.release()
cv2.destroyAllWindows()