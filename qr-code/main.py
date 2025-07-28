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

    #Gray Scale
    gray_img=cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray_img, (3, 3), 0)
    kernel = np.array([[0, -1, 0],
                   [-1, 5,-1],
                   [0, -1, 0]]) 
    


    sharpened = cv.filter2D(blur, -1, kernel)



     # Edge detection
    # Threshold to get binary image
    _, thresh = cv.threshold(sharpened, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    # Invert (if QR code is black on white background)
    inverted = cv.bitwise_not(thresh)

    # Dilate to merge small components (square kernel maintains shape)
    kernel = np.ones((15, 15), np.uint8)
    dilated = cv.dilate(inverted, kernel, iterations=1)

    # Now you can find contours
    contours, _ = cv.findContours(dilated, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    frame_with_contours = frame.copy()

    for cnt in contours:
        area = cv.contourArea(cnt)
        if area > 1500:  # filter out small noise
            cv.drawContours(frame_with_contours, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv.boundingRect(cnt)
            cv.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 4)
    # Show outputs
    cv.imshow("Contours", frame_with_contours)
    cv.imshow("frame", frame)



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