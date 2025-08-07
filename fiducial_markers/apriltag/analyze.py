import cv2 as cv
import numpy as np
import time
from PyQt5.QtCore import QObject, pyqtSignal
from apriltag_detector import detect_apriltag
import math
import numpy as np

class analyze_apriltag(QObject):
    dimension_signal = pyqtSignal(object)
    feed_frame = pyqtSignal(object, list)

    def __init__(self):
        super().__init__()
        self.cap = cv.VideoCapture(0)
        self.previous_time = time.time()
        self.run_program = True
        self.inital_coords = [0, 0]
        self.updated_img = np.zeros((100, 100, 3), np.uint8)

    def run(self):
        while self.run_program:
            ret, self.frame = self.cap.read()
            height, width = self.frame.shape[:2]
            self.tower_order=[]

            if not ret:
                print("Failed to grab frame.")
                break
            
            # Fps calc + display
            current_time = time.time()
            fps = 1 / (current_time - self.previous_time)
            self.previous_time= current_time
            cv.putText(self.updated_img, f"FPS: {fps:.2f}", [self.inital_coords[0] + 10, self.inital_coords[1] + 30], cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            #Gray Scale
            gray_img=cv.cvtColor(self.updated_img, cv.COLOR_BGR2GRAY)
            detections = detect_apriltag(gray_img)

            id_list = []
            tower_dict = {}
            x_tolerance_multiplier = 1 # Will multiply this by the width of the AprilTag perceived in pixels
            y_tolerance_multiplier = 4 # Will multiply this by the height of the AprilTag perceived in pixels

            tallest_coords = 0
            tallest_height = None

            for detection in detections:
                pts = detection["points"]
                bgr_colour = detection["bgr_colour"]
                text_colour = detection["text_colour"]

                center_point = ((pts[0][0] + pts[1][0] + pts[2][0] + pts[3][0]) // 4, (pts[0][1] + pts[1][1] + pts[2][1] + pts[3][1]) // 4)

                if not bgr_colour in id_list:
                    id_list.append([bgr_colour, text_colour, center_point, pts])
                    tower_dict[center_point]=[]
                    
            for bgr_colour, text_colour, (x, y), pts in id_list:
                for existing_x, existing_y in tower_dict.keys():
                    avg_width = (abs((pts[0][0] - pts[1][0])) + abs((pts[2][0] - pts[3][0]))) // 2
                    avg_height = (abs((pts[0][1] - pts[3][1])) + (abs(pts[1][1] - pts[2][1]))) // 2

                    is_within_x = abs(existing_x - x) <= x_tolerance_multiplier * avg_width
                    is_within_y = abs(existing_y - y) <= y_tolerance_multiplier * avg_height
                    has_space_in_tower = len(tower_dict[(existing_x, existing_y)]) < 4
                    
                    tower_colors = [block[0] for block in tower_dict[(existing_x, existing_y)]]
                    color_not_used = bgr_colour not in tower_colors

                    if is_within_x and is_within_y and has_space_in_tower and color_not_used:
                        tower_dict[(existing_x, existing_y)].append([bgr_colour, text_colour, (x, y), pts])
                        tallest_height = 0
                        tallest_coords = None
                        existing_x = x
                        existing_y = y

            if not tallest_height == None:
                for coords, y_list in tower_dict.items():
                    height = len(y_list)

                    if height > tallest_height or height == tallest_height and coords[1] > tallest_coords[1]:
                        tallest_height = height
                        tallest_coords = coords

            if tallest_coords is not None and tallest_coords in tower_dict:
                for bgr_colour, text_colour, y, pts in tower_dict[tallest_coords]:
                    cv.polylines(self.updated_img, [pts], True, bgr_colour, 2)
                    cv.putText(self.updated_img, text_colour, (pts[0][0], pts[0][1] + 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, bgr_colour, 2)
                    self.tower_order.append(text_colour)

               
                cv.putText(self.updated_img, f"Tallest Tower: {tallest_height} blocks", [self.inital_coords[0] + 10, self.inital_coords[1] + 70 ], cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)
                
            # cv.imshow("QR Detection" , frame)
            RGB_frame = cv.cvtColor(self.updated_img, cv.COLOR_BGR2RGB)
            self.feed_frame.emit(RGB_frame, self.tower_order)

            self.dimension_signal.emit("hi")
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv.destroyAllWindows()

    def center_crop_resize(self, target_dimensions):
        h, w, _ = self.frame.shape
        target_width=target_dimensions[0]
        target_height=target_dimensions[1]
        scale = max(target_width / w, target_height / h)
        new_w, new_h = math.ceil(w * scale), math.ceil(h * scale)
        resized = cv.resize(self.frame, (new_w, new_h), interpolation = cv.INTER_AREA)

        x_start = (new_w - target_width) // 2
        y_start = (new_h - target_height) // 2

        cropped = resized[y_start : y_start + target_height, x_start : x_start + target_width]

        self.updated_img = cropped

    def stop(self):
        self.run_program = False
