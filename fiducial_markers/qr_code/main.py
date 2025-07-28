import cv2 as cv
import numpy as np
from qr_code_block_detector import detect_qr

# Open webcam
cap = cv.VideoCapture(0)

zoom_factor = 4 
margin=20.   #unit in pixels

while True:
    success, frame = cap.read()

    height, width = frame.shape[:2]

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
        if area > 2000 and area <100000:  # filter out small noise
            cv.drawContours(frame_with_contours, [cnt], -1, (0, 255, 0), 2)
            x, y, w, h = cv.boundingRect(cnt)

            x_exp = max(x - margin, 0)
            y_exp = max(y - margin, 0)
            x2_exp = min(x + w + margin, width)
            y2_exp = min(y + h + margin, height)


            roi = frame[int(y_exp):int(y2_exp), int(x_exp):int(x2_exp)]
            if roi.size == 0:
                continue
            
            zoomed_roi = cv.resize(roi, ((int(x2_exp) - int(x_exp)) * zoom_factor, (int(y2_exp) - int(y_exp)) * zoom_factor), interpolation=cv.INTER_LINEAR)

            detections = detect_qr(zoomed_roi)

            for detection in detections:
                pts = np.array(detection["points"], dtype=np.float32)
                pts /= zoom_factor

                pts[:, 0] += x_exp
                pts[:, 1] += y_exp
                pts = pts.astype(np.int32)

                color = detection["bgr_colour"]
                cv.polylines(frame, [pts], True, color, 2)
                cv.putText(frame, detection["text_colour"], (pts[0][0], pts[0][1] + 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    cv.imshow("QR Detection", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()