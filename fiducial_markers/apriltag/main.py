import threading
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from main_window import MainWindow
from analyze import analyze_apriltag

def main():
    analyze = analyze_apriltag()
    analyze_thread=threading.Thread(target = analyze.run)
    analyze_thread.start()

    app = QApplication(sys.argv)
    script_directory = os.path.dirname(os.path.abspath(__file__))

    style_path = os.path.join(script_directory, "style.qss")
    with open(style_path) as f:
        app.setStyleSheet(f.read())
    
    window = MainWindow(analyze)
    window.return_dimension.connect(analyze.center_crop_resize)
    window.show()

    exit_code = app.exec_()
    analyze_thread.join()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()  
    