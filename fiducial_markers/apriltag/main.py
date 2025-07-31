import threading
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtCore import QTimer
from main_window import MainWindow
from analyze import analyze
def main():
    analyzer = analyze()
    analyze_thread=threading.Thread(target = analyze.run)
    analyze_thread.start()

    app = QApplication(sys.argv)
    """
    style_path = os.path.join("app", "frontend", "style.qss")
    with open(style_path) as f:
        app.setStyleSheet(f.read())
    """

    window=MainWindow()
    window.show()
    

    exit_code = app.exec_()
    analyze_thread.join()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()  
    