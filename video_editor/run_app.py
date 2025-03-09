import multiprocessing
import sys

from app.application import MainWindow
from PyQt6 import QtWidgets

if __name__ == "__main__":
    # only needed in windows
    # also because we use pyinstaller
    multiprocessing.freeze_support()
    # creates an application instance passing arguments
    app = QtWidgets.QApplication(sys.argv)
    # creates the main window
    window = MainWindow()
    # window show in screen
    window.show()
    # pyqt event loop and exit
    sys.exit(app.exec())
