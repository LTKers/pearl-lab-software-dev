from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget

class MainWindow(QMainWindow):
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


    def initUI(self):
        pass

    def closeEvent(self, event):
        self.analyze.stop()
        return super().closeEvent(event)