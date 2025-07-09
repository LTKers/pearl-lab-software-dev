import cv2 as cv
import numpy as np

capture=cv.VideoCapture(0)
qrdetector=cv.QRCodeDetector()

while True:
    isTrue, frame=capture.read()

    if not isTrue:
        print("frame could not be read")
        break
    
    retval, decoded_info, points, straight_qr = qrdetector.detectAndDecodeMulti(frame)

    if retval:

        for m, p in zip(decoded_info, points):
            colour=m.split(0,-2)
            
            if colour == 'red':
                display_colour=(0, 0, 255)
            elif colour == 'blue':
                display_colour=(255, 0, 0)

            elif colour == 'green':
                 display_colour=(0, 255, 0)

            else:
                 display_colour=(0, 255, 255)

            cv.polylines(frame, points.astype(int), True,  display_colour, 1)
            cv.putText(frame, m, points(0)+(0,50), cv.FONT_HERSHEY_COMPLEX, display_colour, 5)
            
    cv.imshow('qr_code_pose_estimation', frame)

    if  cv.waitKey(20) & 0xFF==ord('d'):
        break


capture.release()
cv.destroyAllWindows()