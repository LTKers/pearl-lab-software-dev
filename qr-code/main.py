import cv2 as cv
import numpy as np
from qr_code_block_detector import detect_qr

# Open webcam
cap = cv.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        print("Failed to grab frame.")
        break


    gray_img=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray_img, (3, 3), 0)
    kernel = np.array([[0, -1, 0],
                   [-1, 5,-1],
                   [0, -1, 0]])

    sharpened = cv.filter2D(blur, -1, kernel)
    ret, bw_im = cv.threshold(sharpened, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    detections = detect_qr(bw_im)

    
    for detection in detections:
        text_colour=detection["text_colour"]
        pts = detection["points"]
        bgr_color = detection["bgr_colour"]

        cv.polylines(frame, [pts], True, bgr_color, 2)
        pt = tuple(pts[0])
        cv.putText(frame, text_colour, (pt[0], pt[1] + 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, bgr_color, 2)

    cv.imshow("QR Detection", frame)

    cv.imshow("bw", bw_im)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()