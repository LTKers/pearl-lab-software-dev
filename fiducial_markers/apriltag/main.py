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

    id_list=[]
    tower_dict={}
    x_tolerance=30
    tallest_x=0
    
    for detection in detections:
        print("yo")
        pts = detection["points"]
        color = detection["bgr_colour"]
        
        center_point = ((pts[0][0] + pts[1][0] + pts[2][0] + pts[3][0])//4, (pts[0][1] + pts[1][1] + pts[2][1] + pts[3][1])//4)

        if not color in id_list:
            id_list.append([color, center_point, pts])
            tower_dict[center_point[0]]=[[center_point[1], pts]]
            
    for color, (x, y), pts in id_list:
        found = False
        for existing_x in list(tower_dict.keys()):
            if abs(existing_x - x) <= x_tolerance:
                tower_dict[existing_x].append([y, pts])

                tallest_height = 0
                tallest_x = None

    for x_coord, y_list in tower_dict.items():
        height = len(y_list)
        if height > tallest_height:
            tallest_height = height
            tallest_x = x_coord

    if tallest_x is not None and tallest_x in tower_dict:
        for y, pts in tower_dict[tallest_x]:
            cv.polylines(frame, [pts], True, color, 2)
        cv.putText(frame, detection["text_colour"], (pts[0][0], pts[0][1] + 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        cv.putText(frame, f"Tallest Tower: {tallest_height} blocks", (10, height - 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                        

        
    cv.imshow("QR Detection", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()