import sys
import cv2
import multiprocessing
from PyQt6 import QtWidgets
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QFileDialog,
    QMessageBox,
)

from app.ui.MainWindow import Ui_MainWindow

from load.loader import file_loader
from export.export_process import export_video_process
from filter.filter_apply import apply_filters
from models.dc_video import DCVideoData, DCFiltersParams, DCVideoExportParams


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
        self.total_frames = 1
        self.export_process = None


        self.video_data = DCVideoData()

    def select_video(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Video", "", "Video Files (*.mp4 *.avi *.mov)"
        )
        if file_name:
            self.video_path = file_name
            self.video_data = file_loader(self.video_path)
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

        frame = apply_filters(
            frame,
            blur_strength,
            canny_threshold,
            sepia_strength,
            brightness_strength,
            saturation_strength,
            sharpen_strength
        )
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

        export_video_process(
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
        )

        QMessageBox.information(
            self, "Export Started", "Video export is running in the background."
        )

    def closeEvent(self, event):
        if self.cap:
            self.cap.release()
        if self.export_process and self.export_process.is_alive():
            self.export_process.terminate()
        event.accept()

