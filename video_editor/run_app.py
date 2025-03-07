import sys
import multiprocessing
from PyQt6 import QtWidgets
from app.application import MainWindow


if __name__ == "__main__":
    multiprocessing.freeze_support()
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
