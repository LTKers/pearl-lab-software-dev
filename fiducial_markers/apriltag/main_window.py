from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QLabel, QSizePolicy, QWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QFontDatabase, QFont, QIcon
from PyQt5.QtCore import Qt, QObject, pyqtSignal

import cv2 as cv
import math

class MainWindow(QMainWindow, QObject):
    dimension_signal = pyqtSignal(list)

    def __init__(self, analyze):
        super().__init__()
        self.setWindowTitle("AprilTag Demo")
        self.initUI()

        self.analyze = analyze

        screen = QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()
        window_width = int(screen_width * 0.6)
        window_height = int(screen_height * 0.6)
        pos_x = (screen_width - window_width) // 2
        pos_y = (screen_height - window_height) // 2
        self.setGeometry(pos_x, pos_y, window_width, window_height)

        self.analyze.feed_frame.connect(self.update_image)

    def initUI(self):

        self.video_feed = QLabel(self)
        self.video_feed.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.video_feed.setMinimumSize(320, 240)  

        central_widget = QWidget()
        self.setCentralWidget(central_widget)   
        self.main_area_layout = QHBoxLayout()
        self.main_area_layout.addWidget(self.video_feed)
        self.main_area_layout.addWidget(self.video_feed)

        central_widget.setLayout(self.main_area_layout)

    def update_image(self, cv_img):
        target_width = self.video_feed.width()
        target_height = self.video_feed.height()

        img = self.center_crop_resize(cv_img, target_width, target_height)

        h, w, ch = img.shape

        bytes_per_line = ch * w
        camera_image = QImage(img.tobytes(), w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_feed.setPixmap(QPixmap.fromImage(camera_image))


    def center_crop_resize(self, frame, target_width, target_height):
        h, w, _ = frame.shape

        scale = max(target_width / w, target_height / h)
        new_w, new_h = math.ceil(w * scale), math.ceil(h * scale)
        resized = cv.resize(frame, (new_w, new_h), interpolation = cv.INTER_AREA)

        x_start = (new_w - target_width) // 2
        y_start = (new_h - target_height) // 2

        cropped = resized[y_start : y_start + target_height, x_start : x_start + target_width]

        orig_x_start = x_start / scale
        orig_y_start = y_start / scale

        self.dimension_signal.emit([orig_x_start, orig_y_start])

        return cropped

    def closeEvent(self, event):
        self.analyze.stop()
        return super().closeEvent(event)