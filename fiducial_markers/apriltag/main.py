import cv2 as cv
import numpy as np
from apriltag_detector import detect_apriltag

# Open webcam
cap = cv.VideoCapture(0)


while True:
    ret, frame = cap.read()
    height, width = frame.shape[:2]

    if not ret:
        print("Failed to grab frame.")
        break

    #Gray Scale
    gray_img=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    detections = detect_apriltag(gray_img)

    for detection in detections:
        print("yo")
        pts = np.array(detection["points"], dtype=np.float32)
        color = detection["bgr_colour"]
        cv.polylines(frame, [pts], True, color, 2)
        cv.putText(frame, detection["text_colour"], (pts[0][0], pts[0][1] + 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    cv.imshow("QR Detection", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()