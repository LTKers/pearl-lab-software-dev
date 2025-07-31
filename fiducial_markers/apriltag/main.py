import cv2 as cv
import numpy as np
import time
from apriltag_detector import detect_apriltag

# Open webcam
cap = cv.VideoCapture(0)
previous_time = time.time()



while True:
    ret, frame = cap.read()
    height, width = frame.shape[:2]

    if not ret:
        print("Failed to grab frame.")
        break
    
     # Fps calc + display
    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time= current_time
    cv.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    #Gray Scale
    gray_img=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    detections = detect_apriltag(gray_img)

    id_list = []
    tower_dict = {}
    x_tolerance_multiplier = 1 # Will multiply this by the width of the AprilTag perceived in pixels
    y_tolerance_multiplier = 4 # Will multiply this by the height of the AprilTag perceived in pixels

    tallest_coords = 0
    tallest_height = None

    for detection in detections:
        pts = detection["points"]
        bgr_colour = detection["bgr_colour"]
        text_colour = detection["text_colour"]

        center_point = ((pts[0][0] + pts[1][0] + pts[2][0] + pts[3][0]) // 4, (pts[0][1] + pts[1][1] + pts[2][1] + pts[3][1]) // 4)

        if not bgr_colour in id_list:
            id_list.append([bgr_colour, text_colour, center_point, pts])
            tower_dict[center_point]=[]
            
    for bgr_colour, text_colour, (x, y), pts in id_list:
        for existing_x, existing_y in tower_dict.keys():
            avg_width = (abs((pts[0][0] - pts[1][0])) + abs((pts[2][0] - pts[3][0]))) // 2
            avg_height = (abs((pts[0][1] - pts[3][1])) + (abs(pts[1][1] - pts[2][1]))) // 2

            if abs(existing_x - x) <= x_tolerance_multiplier * avg_width and abs(existing_y - y) <= y_tolerance_multiplier * avg_height:
                tower_dict[(existing_x, existing_y)].append([bgr_colour, text_colour, (x,y), pts])
                tallest_height = 0
                tallest_coords = None
                existing_x = x
                existing_y = y

    if not tallest_height == None:
        for coords, y_list in tower_dict.items():
            height = len(y_list)

            if height > tallest_height or height == tallest_height and coords[1] > tallest_coords[1]:
                tallest_height = height
                tallest_coords = coords

    if tallest_coords is not None and tallest_coords in tower_dict:
        for bgr_colour, text_colour, y, pts in tower_dict[tallest_coords]:
            cv.polylines(frame, [pts], True, bgr_colour, 2)
            cv.putText(frame, text_colour, (pts[0][0], pts[0][1] + 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, bgr_colour, 2)

        cv.putText(frame, f"Tallest Tower: {tallest_height} blocks", (10, 70), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
        
    cv.imshow("QR Detection", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()