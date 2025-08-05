from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QLabel, QSizePolicy, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QFontDatabase, QFont, QIcon
from PyQt5.QtCore import Qt, QObject, pyqtSignal

import cv2 as cv
import math

class MainWindow(QMainWindow, QObject):
    return_dimension = pyqtSignal(list)

    def __init__(self, analyze):
        super().__init__()
        self.setWindowTitle("AprilTag Demo")
        self.initUI()
        self.tower_list=[]
        self.analyze = analyze

        screen = QDesktopWidget().screenGeometry()
        screen_width = screen.width()
        screen_height = screen.height()
        window_width = int(screen_width * 0.6)
        window_height = int(screen_height * 0.6)
        pos_x = (screen_width - window_width) // 2
        pos_y = (screen_height - window_height) // 2
        self.setGeometry(pos_x, pos_y, window_width, window_height)

        self.analyze.dimension_signal.connect(self.get_dimensions)
        self.analyze.feed_frame.connect(self.update_img)

    def initUI(self):
        self.video_feed = QLabel(self)
        self.video_feed.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.video_feed.setMinimumSize(320, 240)  

        central_widget = QWidget()
        self.setCentralWidget(central_widget)   
        main_area_layout = QHBoxLayout()
        main_area_layout.addWidget(self.video_feed)
        main_area_layout.addWidget(self.video_feed)
        central_widget.setLayout(main_area_layout)

        block_stack = QWidget()
        block_layout = QVBoxLayout()
        block_stack.setLayout(block_layout)

        for i in range(4):
            block_1 = QLabel(self)
            block_pixmap_1 = QPixmap()
            block_1.setPixmap(block_pixmap_1)


    def get_dimensions(self, obj):
        target_width = self.video_feed.width()
        target_height = self.video_feed.height()
        self.return_dimension.emit([target_width, target_height])

    def update_img(self, cv_img, tower_list):
        h, w, ch = cv_img.shape
        bytes_per_line = ch * w
        self.tower_list = tower_list
        camera_image = QImage(cv_img.tobytes(), w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_feed.setPixmap(QPixmap.fromImage(camera_image))
    
    def closeEvent(self, event):
        self.analyze.stop()
        return super().closeEvent(event)