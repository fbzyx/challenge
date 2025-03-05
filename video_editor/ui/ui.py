import sys
import cv2
import numpy as np
import multiprocessing
from PyQt6 import QtWidgets
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QFileDialog,
    QMessageBox,
)

from qt.MainWindow import Ui_MainWindow

from ..export.export_job import video_exporter_job


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setMinimumSize(800, 600)
        self.setupUi(self)

        # Event bindings
        self.btn_select.clicked.connect(self.select_video)
        self.btn_play_pause.clicked.connect(self.play_pause_video)
        self.btn_stop.clicked.connect(self.stop_video)
        self.btn_export.clicked.connect(self.export_video)
        self.slider_blur.valueChanged.connect(self.update_frame)
        self.slider_canny.valueChanged.connect(self.update_frame)
        self.slider_sepia.valueChanged.connect(self.update_frame)
        self.slider_brightness.valueChanged.connect(self.update_frame)
        self.slider_saturation.valueChanged.connect(self.update_frame)
        self.slider_sharpen.valueChanged.connect(self.update_frame)
        self.slider_video.sliderPressed.connect(self.pause_video)  # Pause while seeking
        self.slider_video.sliderReleased.connect(
            self.seek_video
        )  # Resume after seeking

        # Timer for video playback
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.cap = None
        self.is_playing = False
        self.video_path = None
        self.fps = 30
        self.frame_width = 854
        self.frame_height = 480
        self.export_process = None
        self.total_frames = 1

    def select_video(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Video", "", "Video Files (*.mp4 *.avi *.mov)"
        )
        if file_name:
            self.video_path = file_name
            self.cap = cv2.VideoCapture(self.video_path)
            self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.frame_width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.frame_height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.slider_video.setRange(0, self.total_frames)
            self.slider_video.setEnabled(True)  # Enable seek bar
            self.is_playing = False
            self.btn_play_pause.setText("Play")
            self.update_time_label(0)

    def play_pause_video(self):
        if self.cap and self.cap.isOpened():
            if self.is_playing:
                self.timer.stop()
                self.btn_play_pause.setText("Play")
            else:
                self.timer.start(int(1000 / self.fps))
                self.btn_play_pause.setText("Pause")
            self.is_playing = not self.is_playing

    def pause_video(self):
        """Pause the video when the slider is being moved."""
        if self.is_playing:
            self.timer.stop()
            self.is_playing = False
            self.btn_play_pause.setText("Play")

    def stop_video(self):
        if self.cap:
            self.timer.stop()
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.is_playing = False
            self.btn_play_pause.setText("Play")
            self.update_time_label(0)

    def update_time_label(self, current_frame):
        current_time = current_frame / self.fps
        total_time = self.total_frames / self.fps

        current_min, current_sec = divmod(int(current_time), 60)
        total_min, total_sec = divmod(int(total_time), 60)

        self.label_time.setText(
            f"{current_min:02}:{current_sec:02} / {total_min:02}:{total_sec:02}"
        )

    def seek_video(self):
        """Seek video position when the slider is released."""
        if self.cap:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.slider_video.value())
            self.update_frame()
            self.play_pause_video()  # Resume playback

    def update_frame(self):
        if self.cap is None:
            return

        ret, frame = self.cap.read()
        if not ret:
            self.timer.stop()
            self.is_playing = False
            self.btn_play_pause.setText("Play")
            return

        frame = self.apply_filters(frame)

        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_img = QImage(
            frame.data, width, height, bytes_per_line, QImage.Format.Format_BGR888
        )  # Format_RGB888 ?
        pixmap = QPixmap.fromImage(q_img).scaledToHeight(300)
        self.label_video.setPixmap(pixmap)
        # Update seek bar
        current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
        self.slider_video.setValue(current_frame)
        self.update_time_label(current_frame)

    def apply_filters(self, frame):
        blur_strength = self.slider_blur.value()
        canny_threshold = self.slider_canny.value()
        sepia_strength = self.slider_sepia.value()
        brightness_strength = self.slider_brightness.value()
        saturation_strength = self.slider_saturation.value()
        sharpen_strength = self.slider_sharpen.value()

        # Apply Blur
        if blur_strength > 0:
            frame = cv2.GaussianBlur(
                frame, (2 * blur_strength + 1, 2 * blur_strength + 1), 0
            )

        # Apply Canny Edge Detection
        if canny_threshold > 0:
            edges = cv2.Canny(frame, canny_threshold, canny_threshold * 2)
            frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # Apply Sepia
        if sepia_strength > 0:
            sepia_matrix = np.array(
                [[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]]
            )
            sepia_filter = (sepia_strength / 100.0) * sepia_matrix + (
                1 - sepia_strength / 100.0
            ) * np.eye(3)
            frame = cv2.transform(frame, sepia_filter)
            frame = np.clip(frame, 0, 255).astype(np.uint8)

        if brightness_strength != 0:
            frame = np.clip(
                frame.astype(np.int16) + brightness_strength, 0, 255
            ).astype(np.uint8)

        if saturation_strength != 0:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            hsv[:, :, 1] = np.clip(
                hsv[:, :, 1].astype(np.int16) + saturation_strength, 0, 255
            )
            frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        if sharpen_strength > 0:
            kernel = np.array([[0, -1, 0], [-1, 5 + sharpen_strength, -1], [0, -1, 0]])
            frame = cv2.filter2D(frame, -1, kernel)

        return frame

    def export_video(self):
        if not self.video_path:
            QMessageBox.warning(
                self, "No Video Selected", "Please select a video first."
            )
            return

        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Processed Video", "", "MP4 Files (*.mp4)"
        )
        if not save_path:
            return

        # Run export in background process
        self.export_process = multiprocessing.Process(
            target=export_video_process,
            args=(
                self.video_path,
                save_path,
                self.fps,
                (self.frame_width, self.frame_height),
                self.slider_blur.value(),
                self.slider_canny.value(),
                self.slider_sepia.value(),
                self.slider_brightness.value(),
                self.slider_saturation.value(),
                self.slider_sharpen.value(),
            ),
        )
        self.export_process.start()

        QMessageBox.information(
            self, "Export Started", "Video export is running in the background."
        )

    def closeEvent(self, event):
        if self.cap:
            self.cap.release()
        if self.export_process and self.export_process.is_alive():
            self.export_process.terminate()
        event.accept()
