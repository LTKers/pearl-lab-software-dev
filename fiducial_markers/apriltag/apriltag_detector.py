"""
AprilTag's and their respective blocks
The AprilTags come from the family tag16h5.
The list of AprilTags can be found here https://github.com/AprilRobotics/apriltag-imgs

ID  BLOCK
1   Blue
2   Green
3   Red
4   Yellow

"""

import cv2 as cv
import pupil_apriltags as pat

apriltag_detector = pat.Detector(family='tag16h5')

def detect_apriltag(frame):
    detections = apriltag_detector.detect(frame, estimate_tag_pose=False)
    
    results = []
    for detection in detections:
        print("hi")
        if detection.tag_id == 0:
            text_colour = 'blue';
            bgr_colour = (0, 0, 255)
            text_colour = 'red';
            bgr_colour = (0, 0, 255)

        elif detection.tag_id == 1:
            text_colour = 'Green';
            bgr_colour = (0, 255, 0)

        elif detection.tag_id == 2:
            text_colour = 'red';
            bgr_colour = (0, 0, 255)

        elif detection.tag_id == 3:
            text_colour = 'Yellow';
            bgr_colour = (0, 255, 255)

        results.append({
            "text_colour": text_colour,
            "bgr_colour": bgr_colour,
            "points": detection.corners.astype(int)
        })

    return results
