import cv2 as cv
from qr_code_block_detector import detect_qr

# Open webcam
cap = cv.VideoCapture(0)

while True:
    success, frame = cap.read()
    if not success:
        print("Failed to grab frame.")
        break

    detections = detect_qr(frame)

    for detection in detections:
        text_colour=detection["text_colour"]
        pts = detection["points"]
        bgr_color = detection["bgr_color"]

        cv.polylines(frame, [pts], True, bgr_color, 2)
        pt = tuple(pts[0])
        cv.putText(frame, text_colour, (pt[0], pt[1] + 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, bgr_color, 2)

    cv.imshow("QR Detection", frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()