import cv2
from PyQt6 import QtWidgets
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QFileDialog,
    QMessageBox,
)

from app.ui.MainWindow import Ui_MainWindow

from load.load import file_loader
from export.process import export_process
from filter.filter_frame import get_filtered_frame
from models.dc_video import DCVideoData, DCFiltersParams, DCVideoExportParams


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        # self.setMinimumSize(800, 600)
        self.setupUi(self)

        # Event bindings
        self.btn_select.clicked.connect(self.select_video_file)
        self.btn_play_pause.clicked.connect(self.play_pause_video)
        self.btn_stop.clicked.connect(self.stop_video)
        self.btn_export.clicked.connect(self.export_video_to_file)
        self.slider_blur.valueChanged.connect(self.update_frame_according_state)
        self.slider_canny.valueChanged.connect(self.update_frame_according_state)
        self.slider_sepia.valueChanged.connect(self.update_frame_according_state)
        self.slider_brightness.valueChanged.connect(self.update_frame_according_state)
        self.slider_saturation.valueChanged.connect(self.update_frame_according_state)
        self.slider_sharpen.valueChanged.connect(self.update_frame_according_state)
        self.slider_video.sliderPressed.connect(self.pause_video)  # Pause while seeking
        self.slider_video.sliderReleased.connect(
            self.move_video_to_slider_position
        )  # Resume after seeking

        # Timer for video playback
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame_according_state)

        self.is_playing = False
        self.export_process = None
        self.last_playing_frame = None
        self.first_frame = None
        self.video_data = DCVideoData()

    def select_video_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Video", "", "Video Files (*.mp4 *.avi *.mov)"
        )
        if file_name:
            self.video_data.input_path = file_name
            self.video_data = file_loader(self.video_data)
            self.slider_video.setRange(0, self.video_data.total_frames)
            self.slider_video.setValue(0)
            self.slider_video.setEnabled(True)  # Enable seek bar
            self.is_playing = False
            self.btn_play_pause.setText("Play")
            self.update_time_label(0)

            ## get first frame
            ret, frame = self.video_data.cap.read()
            self.last_playing_frame = frame
            self.first_frame = frame
            self.get_filter_values_and_apply_to_frame(frame)
            self.update_video_in_ui(frame)

    def play_pause_video(self):
        if self.video_data.cap and self.video_data.cap.isOpened():
            if self.is_playing:
                self.timer.stop()
                self.btn_play_pause.setText("Play")
            else:
                self.timer.start(int(1000 / self.video_data.fps))
                self.btn_play_pause.setText("Pause")
            self.is_playing = not self.is_playing

    def pause_video(self):
        """Pause the video when the slider is being moved."""
        if self.is_playing:
            self.timer.stop()
            self.is_playing = False
            self.btn_play_pause.setText("Play")

    def stop_video(self):
        if self.video_data.cap:
            self.timer.stop()
            self.video_data.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.is_playing = False
            self.btn_play_pause.setText("Play")
            self.update_time_label(0)
            self.slider_video.setValue(0)
            ##### change behaviour
            self.update_video_in_ui(self.first_frame)
            self.last_playing_frame = self.first_frame

    def update_time_label(self, current_frame):
        current_time = current_frame / self.video_data.fps
        total_time = self.video_data.total_frames / self.video_data.fps

        current_min, current_sec = divmod(int(current_time), 60)
        total_min, total_sec = divmod(int(total_time), 60)

        self.label_time.setText(
            f"{current_min:02}:{current_sec:02} / {total_min:02}:{total_sec:02}"
        )

    def move_video_to_slider_position(self):
        """Seek video position when the slider is released."""
        if self.video_data.cap:
            self.video_data.cap.set(cv2.CAP_PROP_POS_FRAMES, self.slider_video.value())
            self.update_frame_according_state()
            self.play_pause_video()  # Resume playback

    def update_video_in_ui(self, frame):
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_img = QImage(
            frame.data,
            width,
            height,
            bytes_per_line,
            QImage.Format.Format_BGR888,
        )  # Format_RGB888 ?
        pixmap = QPixmap.fromImage(q_img).scaledToHeight(
            300
        )

        # pixmap = QPixmap.fromImage(q_img).scaledToHeight(
        #     (self.label_video.height())
        # )

        self.label_video.setPixmap(pixmap)

        if self.is_playing:
            # Update seek bar
            current_frame = int(self.video_data.cap.get(cv2.CAP_PROP_POS_FRAMES))
            self.slider_video.setValue(current_frame)
            self.update_time_label(current_frame)

    def update_frame_according_state(self):
        if self.video_data.cap is None:
            return

        if not self.is_playing:
            frame = self.get_filter_values_and_apply_to_frame(self.last_playing_frame)
            self.update_video_in_ui(frame)
            return

        ret, frame = self.video_data.cap.read()
        if not ret:
            self.timer.stop()
            self.is_playing = False
            self.btn_play_pause.setText("Play")
            return

        self.last_playing_frame = frame
        frame = self.get_filter_values_and_apply_to_frame(frame)
        self.update_video_in_ui(frame)

    def get_filter_values_from_widgets(self) -> DCFiltersParams:
        dc_filter_params = DCFiltersParams(
            blur_strength=self.slider_blur.value(),
            canny_threshold=self.slider_canny.value(),
            sepia_strength=self.slider_sepia.value(),
            brightness_strength=self.slider_brightness.value(),
            saturation_strength=self.slider_saturation.value(),
            sharpen_strength=self.slider_sharpen.value(),
        )
        return dc_filter_params

    def get_filter_values_and_apply_to_frame(self, frame):
        dc_filter_params = self.get_filter_values_from_widgets()
        return get_filtered_frame(frame, dc_filter_params)

    def export_video_to_file(self):
        if not self.video_data.input_path:
            QMessageBox.warning(
                self, "No Video Selected", "Please select a video first."
            )
            return

        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Processed Video", "", "MP4 Files (*.mp4)"
        )

        dc_filter_params = self.get_filter_values_from_widgets()

        dc_video_data_for_proc = DCVideoData(
            fps=self.video_data.fps,
            frame_size=self.video_data.frame_size,
            total_frames=self.video_data.total_frames,
            input_path=self.video_data.input_path,
        )
        dc_export_params_data_for_proc = DCVideoExportParams(
            video_data=dc_video_data_for_proc,
            filter_params=dc_filter_params,
            output_path=save_path,
        )

        self.export_process = export_process(dc_export_params_data_for_proc)

        QMessageBox.information(
            self, "Export Started", "Video export is running in the background."
        )

    def closeEvent(self, event):
        if self.video_data.cap:
            self.video_data.cap.release()
        if self.export_process:
            if self.export_process.is_alive():
                self.export_process.terminate()
        event.accept()
