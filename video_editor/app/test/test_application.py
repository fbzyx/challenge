import sys
import unittest

from PyQt6.QtWidgets import QApplication

from app.application import MainWindow


class TestMainWindow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the application instance before running tests."""
        cls.app = QApplication(sys.argv)

    def setUp(self):
        """Create a new instance of MainWindow before each test."""
        self.window = MainWindow()
        self.window.show()

    def tearDown(self):
        """Close the window after each test."""
        self.window.close()

    def test_ui_initialization(self):
        """Test if the UI elements are properly initialized."""
        self.assertIsNotNone(self.window.btn_select)
        self.assertIsNotNone(self.window.btn_play_pause)
        self.assertIsNotNone(self.window.btn_export)
        self.assertIsNotNone(self.window.btn_stop)
        self.assertIsNotNone(self.window.label_video)
        self.assertIsNotNone(self.window.label_resolution)
        self.assertIsNotNone(self.window.label_fps)
        self.assertIsNotNone(self.window.label_blur)
        self.assertIsNotNone(self.window.label_brightness)
        self.assertIsNotNone(self.window.label_canny)
        self.assertIsNotNone(self.window.label_sepia)
        self.assertIsNotNone(self.window.label_sharpen)
        self.assertIsNotNone(self.window.label_saturation)
        self.assertIsNotNone(self.window.label_hue)
        self.assertIsNotNone(self.window.label_time)
        self.assertIsNotNone(self.window.slider_blur)
        self.assertIsNotNone(self.window.slider_canny)
        self.assertIsNotNone(self.window.slider_sepia)
        self.assertIsNotNone(self.window.slider_sharpen)
        self.assertIsNotNone(self.window.slider_saturation)
        self.assertIsNotNone(self.window.slider_brightness)
        self.assertIsNotNone(self.window.slider_video)
        self.assertIsNotNone(self.window.dial_hue)

    @classmethod
    def tearDownClass(cls):
        """Close the application instance after tests."""
        cls.app.quit()


if __name__ == "__main__":
    unittest.main()
