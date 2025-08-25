"""
AprilTag's and their respective blocks
The AprilTags come from the family tag16h5.
The list of AprilTags can be found here https://github.com/AprilRobotics/apriltag-imgs

ID  BLOCK
1   Blue_1
2   Blue_2
3   Green_1
4   Green_2
5   Red_1
6   Red_2
7   Yellow_1
8   Yellow_2

This script runs the pupil_apriltags library detection with basic margin/confidence and ID filtering.
"""

import cv2 as cv
import pupil_apriltags as pat

apriltag_detector = pat.Detector(
    families='tag16h5',
    nthreads=1,              
    quad_decimate=1.0,       
    quad_sigma=0.8,          
    refine_edges=1  ,       
    decode_sharpening=1, 
    debug=0                  
)


def detect_apriltag(frame):
    detections = apriltag_detector.detect(frame, estimate_tag_pose = False)
    
    results = []
    for detection in detections:
        if detection.decision_margin > 50 and detection.tag_id < 9:
            if detection.tag_id == 0:
                text_colour = 'Blue_2';
                bgr_colour = (255, 0, 0)

            elif detection.tag_id == 1:
                text_colour = 'Blue_2';
                bgr_colour = (255, 0, 0)

            elif detection.tag_id == 2:
                text_colour = 'Green_1';
                bgr_colour = (0, 255, 0)

            elif detection.tag_id == 3:
                text_colour = 'Green_2';
                bgr_colour = (0, 255, 0)

            elif detection.tag_id == 4:
                text_colour = 'Red_1';
                bgr_colour = (0, 0, 255)

            elif detection.tag_id == 5:
                text_colour = 'Red_2';
                bgr_colour = (0, 0, 255)

            elif detection.tag_id == 6:
                text_colour = 'Yellow_1';
                bgr_colour = (0, 255, 255)

            elif detection.tag_id == 7:
                text_colour = 'Yellow_2';
                bgr_colour = (0, 255, 255)

            else:
                text_colour = 'null';
                bgr_colour = (0, 0, 0)
            
            results.append({
                "text_colour": text_colour,
                "bgr_colour": bgr_colour,
                "points": detection.corners.astype(int),
                "decision_margin": detection.decision_margin
            })

    return results
