from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget, QLabel, QSizePolicy, QWidget, QHBoxLayout, QVBoxLayout, QBoxLayout, QGridLayout, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap, QImage, QFontDatabase, QFont, QIcon
from PyQt5.QtCore import Qt, QObject, pyqtSignal
import cv2 as cv
import math
import os

# GUI Design

class MainWindow(QMainWindow, QObject):
    return_dimension = pyqtSignal(list)

    def __init__(self, analyze):
        super().__init__()
        self.setWindowTitle("AprilTag Demo")
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

        self.initUI()


    def initUI(self):
        self.video_feed = QLabel(self)
        self.video_feed.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.video_feed.setMinimumSize(320, 240)  

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)   
        main_area_layout = QHBoxLayout()
        main_area_layout.addWidget(self.video_feed)
        self.central_widget.setLayout(main_area_layout)

        self.right_area = QWidget()
        self.right_area_layout = QVBoxLayout()
        self.right_area.setLayout(self.right_area_layout)
        main_area_layout.addWidget(self.right_area)
        self.right_area.setFixedWidth(200)

        self.top_right_area = QWidget()
        self.top_right_area_layout=QHBoxLayout()
        self.top_right_area.setLayout(self.top_right_area_layout)
        self.top_right_area.setObjectName("top_right_area")
        self.top_right_area.setFixedHeight(100)
        self.right_area_layout.addWidget(self.top_right_area)

        self.title = QLabel("AprilTag Demo", self)
        self.top_right_area_layout.addWidget(self.title)
        self.title.setObjectName("title")

        self.block_stack = QWidget()
        block_layout = QVBoxLayout()
        self.block_stack.setLayout(block_layout)
        block_layout.setDirection(QBoxLayout.BottomToTop)
        self.right_area_layout.addWidget(self.block_stack)

        self.blocks = []
        self.block_pxmaps = []

        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.red = QPixmap(os.path.join(script_directory, "images", "web_blocks", "red.png"))
        self.blue = QPixmap(os.path.join(script_directory, "images", "web_blocks", "blue.png"))
        self.yellow = QPixmap(os.path.join(script_directory, "images", "web_blocks", "yellow.png"))
        self.green = QPixmap(os.path.join(script_directory, "images", "web_blocks", "green.png"))
        self.transparent = QPixmap(os.path.join(script_directory, "images", "web_blocks", "transparent.png"))

        self.settings_area = QWidget()
        self.settings_layout = QGridLayout()
        self.settings_area.setLayout(self.settings_layout)
        self.settings_layout.setVerticalSpacing(10)
        self.settings_area.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.right_area_layout.addWidget(self.settings_area, alignment=Qt.AlignBottom)

        for i in range(4):
            block_label = QLabel(self)
            block_label.setPixmap(self.transparent)
            block_label.setFixedSize(100, 100)
            block_layout.addWidget(block_label)
            self.blocks.append(block_label)

        self.resolution_text = QLabel("Resolution")
        self.settings_layout.addWidget(self.resolution_text, 0, 0)

        self.width_text = QLabel("Width (px):")
        self.width_input = QLineEdit()
        self.settings_layout.addWidget(self.width_text, 1, 0)
        self.settings_layout.addWidget(self.width_input, 1, 1)
        self.width_input.editingFinished.connect(lambda: self.validate_res(self.width_input.text(), self.width_input))

        self.height_text = QLabel("Height (px):")
        self.height_input = QLineEdit()
        self.settings_layout.addWidget(self.height_text, 2, 0)
        self.settings_layout.addWidget(self.height_input, 2, 1)
        self.height_input.editingFinished.connect(lambda: self.validate_res(self.height_input.text(), self.height_input))

        self.set_res = QPushButton("Set Resolution", self)
        self.set_res.adjustSize()

        self.set_res.setObjectName("set_res")
        self.settings_layout.addWidget(self.set_res, 3, 0)
        self.set_res.clicked.connect(
            lambda: self.analyze.update_res(
                int(self.width_input.text() or 0),
                int(self.height_input.text() or 0)
            )
        )

        self.error_text = QLabel("")
        self.error_text.setObjectName("error")
        self.settings_layout.addWidget(self.error_text)

    # Communication between gui and analyze.py.
    def get_dimensions(self, obj):
        target_width = self.video_feed.width()
        target_height = self.video_feed.height()
        self.return_dimension.emit([target_width, target_height])

    # Img needs to be cropped from center.
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

    # Makes sure all threads are stopped
    def closeEvent(self, event):
        self.analyze.stop()
        return super().closeEvent(event)
    
    # Ensure resolution set is appropriate
    def validate_res(self, value, input_field):
        if not value.isdigit() or int(value) < 0:
            input_field.setText("100")
            self.error_text.setText("ERROR")
        else:
            self.error_text.setText("")

            
        

