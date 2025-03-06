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
from app.resize_handler import resize_handler

import multiprocessing
from typing import Optional


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
        self.slider_blur.valueChanged.connect(self.update_frame_according_app_state)
        self.slider_canny.valueChanged.connect(self.update_frame_according_app_state)
        self.slider_sepia.valueChanged.connect(self.update_frame_according_app_state)
        self.slider_brightness.valueChanged.connect(
            self.update_frame_according_app_state
        )
        self.slider_saturation.valueChanged.connect(
            self.update_frame_according_app_state
        )
        self.slider_sharpen.valueChanged.connect(self.update_frame_according_app_state)
        self.slider_video.sliderPressed.connect(self.pause_video)  # Pause while seeking
        self.slider_video.sliderReleased.connect(
            self.move_video_to_slider_position
        )  # Resume after seeking

        self.statusbar.showMessage("Ready")

        # Timer for video playback
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame_according_app_state)

        self.is_playing = False
        self.export_process: Optional[multiprocessing.Process] = None
        self.last_playing_frame = None
        self.first_frame = None
        self.video_data = DCVideoData()

    def resizeEvent(self, event):
        """
        Callback function called when window is resized.
        :param event:
        :return: None
        """
        resize_handler()

    def select_video_file(self):
        """
        Callback function called when btn is pressed to select a new video.
        The purpose is to load a new video and store all video values
        like fps, frame count, etc. It also resets the ui components and values.
        :return: None
        """

        # get input file filename
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Video", "", "Video Files (*.mp4 *.avi *.mov)"
        )
        # if a file is selected
        if file_name:
            # store input path in data object
            self.video_data.input_path = file_name
            # call function to load the video and its parameters
            self.video_data = file_loader(self.video_data)
            # display video input path at bottom of ui
            self.statusbar.showMessage(self.video_data.input_path)
            # set the range for the video position slider according to frame count
            self.slider_video.setRange(0, self.video_data.total_frames)
            # set start slider position to start (or reset position)
            self.slider_video.setValue(0)
            # enable the slider
            self.slider_video.setEnabled(True)
            # set is_playing flag to false
            self.is_playing = False
            # set text "play" in btn
            self.btn_play_pause.setText("Play")
            # set time label back to 00:00
            self.update_time_label(0)

            # get only first frame for display in video area
            # as video placeholder until video is started
            ret, frame = self.video_data.cap.read()
            # store as last playing frame
            self.last_playing_frame = frame
            # store also as first frame
            self.first_frame = frame
            # apply filter values from sliders
            frame = self.get_filter_values_and_apply_to_frame(frame)
            # put first filtered frame in video ui place.
            self.update_video_in_ui(frame)

    def play_pause_video(self):
        """
        Callback function called when play or pause btn is pressed.
        Purpose is play and pause the video.
        :return: None
        """

        # if there is a video and the file is open
        if self.video_data.cap and self.video_data.cap.isOpened():
            # if it is playing (is_playing = True)
            if self.is_playing:
                # stop the timer (This timer calls a function for updating video frames)
                self.timer.stop()
                # Now video is paused, new label of btn should be "Play"
                self.btn_play_pause.setText("Play")
            else:
                # if video is paused, set time with timeout according to fps
                # This timer calls a function for updating video frames
                self.timer.start(int(1000 / self.video_data.fps))
                # Now video is playing, new label of btn should be "Pause"
                self.btn_play_pause.setText("Pause")
            # Toggle state of is_playing flag (self.is_playing = False at start)
            self.is_playing = not self.is_playing

    def pause_video(self):
        """
        Pause the video.
        :return: None
        """
        # if video is playing, stop the video
        if self.is_playing:
            # stop the timer (This timer calls a function for updating video frames)
            self.timer.stop()
            # set flag state
            self.is_playing = False
            # set btn text
            self.btn_play_pause.setText("Play")

    def stop_video(self):
        """
        Stop the video.
        Reset some values to start again.
        :return: None
        """

        # if there is a video
        if self.video_data.cap:
            # stop the timer (This timer calls a function for updating video frames)
            self.timer.stop()
            # set property identifier to 0. In this case:
            # CAP_PROP_POS_FRAMES: 0-based index of the frame to be decoded/captured next. (from docs)
            self.video_data.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            # set flag state to not playing
            self.is_playing = False
            # set btn text accordingly
            self.btn_play_pause.setText("Play")
            # reset the time to 00:00 since video was paused
            self.update_time_label(0)
            # reset the slider to o since video was paused
            self.slider_video.setValue(0)
            ##### change behaviour #####
            # Display first frame again
            # self.update_video_in_ui(self.first_frame)
            # set last shown frame to first video frame
            # self.last_playing_frame = self.first_frame

    def update_time_label(self, current_frame):
        """
        Function called to change the time label shown in the ui
        depending on current video frame
        :param current_frame:
        :return: None
        """

        # get current seconds calculated from fps (frame per second) and current_frame
        current_time = current_frame / self.video_data.fps
        # calculate current video total length
        total_time = self.video_data.total_frames / self.video_data.fps

        # get elapsed time.
        # divmod returns a tuple containing the quotient  and the remainder
        # when argument1 (dividend) is divided by argument2 (divisor)
        current_min, current_sec = divmod(int(current_time), 60)
        # get minutes and seconds from total time
        total_min, total_sec = divmod(int(total_time), 60)
        # display in ui accordingly to time values
        self.label_time.setText(
            f"{current_min:02}:{current_sec:02} / {total_min:02}:{total_sec:02}"
        )

    def move_video_to_slider_position(self):
        """
        Move the video accordingly to slider position
        :return: None
        """
        # if there is a video
        if self.video_data.cap:
            # set CAP_PROP_POS_FRAMES property to slider value
            self.video_data.cap.set(cv2.CAP_PROP_POS_FRAMES, self.slider_video.value())
            # update frame shown in ui according app state and filter values
            self.update_frame_according_app_state()
            # resume video playback (video is paused with callback when slider is clicked)
            self.play_pause_video()

    def update_video_in_ui(self, frame):
        """

        :param frame:
        :return:
        """
        height, width, channel = frame.shape
        bytes_per_line = 3 * width
        q_img = QImage(
            frame.data,
            width,
            height,
            bytes_per_line,
            QImage.Format.Format_BGR888,
        )  # Format_RGB888 ?
        pixmap = QPixmap.fromImage(q_img).scaledToHeight(300)

        # pixmap = QPixmap.fromImage(q_img).scaledToHeight(
        #     (self.label_video.height())
        # )

        self.label_video.setPixmap(pixmap)

        if self.is_playing:
            # Update video position bar
            current_frame = int(self.video_data.cap.get(cv2.CAP_PROP_POS_FRAMES))
            self.slider_video.setValue(current_frame)
            self.update_time_label(current_frame)

    def update_frame_according_app_state(self):

        # if no video capture (cv2.VideoCapture) then do nothing and return
        if self.video_data.cap is None:
            return

        # if the app is not playing but this function was called, then just take the last
        # frame and apply the filters and update the ui to show the filtered frame.
        # This is the case when the video is paused but the filter slider calls this function (by callback).
        if not self.is_playing:
            # filter last frame
            frame = self.get_filter_values_and_apply_to_frame(self.last_playing_frame)
            # pass filterd frame to ui update function
            self.update_video_in_ui(frame)
            return

        # check if video is playing. Get next frame.
        ret, frame = self.video_data.cap.read()
        # if no data
        if not ret:
            self.timer.stop()
            # set is_playing flag to false
            self.is_playing = False
            # change btn to show "play" text
            self.btn_play_pause.setText("Play")
            return

        # Store the last frame
        self.last_playing_frame = frame
        # filter last frame
        frame = self.get_filter_values_and_apply_to_frame(frame)
        # pass filterd frame to ui update function
        self.update_video_in_ui(frame)

    def get_filter_values_from_widgets(self) -> DCFiltersParams:
        """
        Function that read current values from filter sliders.
        :return: DCFiltersParams, Dataclass object with all filter values.
        """

        # read and put values in dataclass
        dc_filter_params = DCFiltersParams(
            blur_strength=self.slider_blur.value(),
            canny_threshold=self.slider_canny.value(),
            sepia_strength=self.slider_sepia.value(),
            brightness_strength=self.slider_brightness.value(),
            saturation_strength=self.slider_saturation.value(),
            sharpen_strength=self.slider_sharpen.value(),
        )
        # return
        return dc_filter_params

    def get_filter_values_and_apply_to_frame(self, frame):
        """
        Function that call other function to read filter values from sliders.
        With the filter values other function is called to filter the frame.
        :param frame: frame to be filtered
        :return: filtered frame
        """
        # get filter values from sliders
        dc_filter_params = self.get_filter_values_from_widgets()
        # call fnc for filtering with slider values and return filtered frame
        return get_filtered_frame(frame, dc_filter_params)

    def export_video_to_file(self):
        """
        Callback function called when export btn is pressed.
        Gets the values needed for the export process and calls
        the function to start the subprocess.
        :return:
        """

        # if btn is pressed but we dont have a video file loaded
        # input_path that was set when we loaded the last file (fnc select_video_file),
        if not self.video_data.input_path:
            # Show an ui warning message to user and return
            QMessageBox.warning(
                self, "No Video Selected", "Please select a video first."
            )
            return

        # get the output filename.
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Processed Video", "", "MP4 Files (*.mp4)"
        )

        # TODO return when cancel btn is pressed

        # get current filter values from sliders
        dc_filter_params = self.get_filter_values_from_widgets()

        # do a copy of current video parameters stored in self.video_data
        # these parameters where set in video load function
        dc_video_data_for_proc = DCVideoData(
            fps=self.video_data.fps,
            frame_size=self.video_data.frame_size,
            total_frames=self.video_data.total_frames,
            input_path=self.video_data.input_path,
        )
        # Put video parameters, filter values and output path together in data object
        dc_export_params_data_for_proc = DCVideoExportParams(
            video_data=dc_video_data_for_proc,
            filter_params=dc_filter_params,
            output_path=save_path,
        )

        # pass data object with all parameters to function for starting process in background
        self.export_process = export_process(dc_export_params_data_for_proc)

        # Display message to user that export process is running in background
        QMessageBox.information(
            self, "Export Started", "Video export is running in the background."
        )

    def closeEvent(self, event):
        """
        Callback function when app is closed.
        :param event:
        :return:
        """
        # if video file is open
        if self.video_data.cap:
            # closes video file
            self.video_data.cap.release()
        # if export process is running
        if self.export_process:
            if self.export_process.is_alive():
                # end the process
                self.export_process.terminate()
        event.accept()
