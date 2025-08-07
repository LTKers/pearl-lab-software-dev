from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QLabel, QSizePolicy, QWidget, QHBoxLayout, QVBoxLayout, QBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QFontDatabase, QFont, QIcon
from PyQt5.QtCore import Qt, QObject, pyqtSignal
import cv2 as cv
import math
import os

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
        self.analyze.feed_frame.connect(self.update_window)

    def initUI(self):
        self.video_feed = QLabel(self)
        self.video_feed.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.video_feed.setMinimumSize(320, 240)  

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)   
        main_area_layout = QHBoxLayout()
        main_area_layout.addWidget(self.video_feed)
        self.central_widget.setLayout(main_area_layout)

        self.block_stack = QWidget()
        block_layout = QVBoxLayout()
        self.block_stack.setLayout(block_layout)
        block_layout.setDirection(QBoxLayout.BottomToTop)
        main_area_layout.addWidget(self.block_stack)

        self.blocks = []
        self.block_pxmaps = []

        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.red = QPixmap(os.path.join(script_directory, "images", "web_blocks", "red.png"))
        self.blue = QPixmap(os.path.join(script_directory, "images", "web_blocks", "blue.png"))
        self.yellow = QPixmap(os.path.join(script_directory, "images", "web_blocks", "yellow.png"))
        self.green = QPixmap(os.path.join(script_directory, "images", "web_blocks", "green.png"))
        self.transparent = QPixmap(os.path.join(script_directory, "images", "web_blocks", "transparent.png"))

        for i in range(4):
            block_label = QLabel(self)
            block_label.setPixmap(self.transparent)
            block_label.setFixedSize(100, 100)
            block_layout.addWidget(block_label)
            self.blocks.append(block_label)

      
    def get_dimensions(self, obj):
        target_width = self.video_feed.width()
        target_height = self.video_feed.height()
        self.return_dimension.emit([target_width, target_height])

    def update_window(self, cv_img, tower_list):
        h, w, ch = cv_img.shape
        bytes_per_line = ch * w
        self.tower_list = tower_list
        camera_image = QImage(cv_img.tobytes(), w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_feed.setPixmap(QPixmap.fromImage(camera_image))

        for i in range (4):
            color = self.tower_list[i] if i < len(self.tower_list) else ""
            self.setBlockImg(color, i)

    def setBlockImg(self, colour, index):
        print(colour[0:-2])
        match colour[0:-2]:
            case "Red":
                self.blocks[index].setPixmap(self.red)

            case "Blue":
                self.blocks[index].setPixmap(self.blue)

            case "Yellow":
                self.blocks[index].setPixmap(self.yellow)

            case "Green":
                self.blocks[index].setPixmap(self.green)
            
            case _:
                self.blocks[index].setPixmap(self.transparent)

    def closeEvent(self, event):
        self.analyze.stop()
        return super().closeEvent(event)