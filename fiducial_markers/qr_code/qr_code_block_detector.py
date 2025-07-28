import cv2 as cv
import numpy as np

qr_detector = cv.QRCodeDetector()

def detect_qr(frame):
    retval, decoded_info, points, _ = qr_detector.detectAndDecodeMulti(frame)
    results = []

    if retval:
        for message, corner_points in zip(decoded_info, points):

            text_colour = message.split("_")[0]

            if text_colour == 'red':
                bgr_colour = (0, 0, 255)
            elif text_colour == 'blue':
                bgr_colour = (255, 0, 0)
            elif text_colour == 'green':
                bgr_colour = (0, 255, 0)
            else:
                bgr_colour = (0, 255, 255)

            results.append({
                "text_colour": text_colour,
                "bgr_colour": bgr_colour,
                "points": corner_points.astype(int)
            })

    return results