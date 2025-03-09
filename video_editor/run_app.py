import multiprocessing
import sys

from app.application import MainWindow
from PyQt6 import QtWidgets

if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
