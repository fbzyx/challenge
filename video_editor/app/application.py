import multiprocessing
from typing import Optional

import cv2
import numpy.typing as npt
from export.process import export_process
from filter.filter_frame import get_filtered_frame
from load.load import file_loader
from models.dc_video import (
    DCFiltersParams,
    DCVideoData,
    DCVideoExportParams,
)
from models.type_dialogs import TypeDialog
from models.type_status import (
    TypeLoadStatus,
    TypeVideoTypeStatus,
)
from PyQt6 import QtWidgets
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import (
    QFileDialog,
    QMessageBox,
)

from app.ui.MainWindow import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    """
    This class represents the Qt Application
    """

    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)

        # event with callback bindings
        self.btn_select.clicked.connect(self.select_video_file)
        self.btn_play_pause.clicked.connect(self.play_pause_video)
        self.btn_stop.clicked.connect(self.stop_video)
        self.btn_export.clicked.connect(self.export_video_to_file)
        # filter slider events
        self.slider_blur.valueChanged.connect(self.callback_filter_update)
        self.slider_canny.valueChanged.connect(self.callback_filter_update)
        self.slider_sepia.valueChanged.connect(self.callback_filter_update)
        self.slider_brightness.valueChanged.connect(self.callback_filter_update)
        self.slider_saturation.valueChanged.connect(self.callback_filter_update)
        self.slider_sharpen.valueChanged.connect(self.callback_filter_update)
        # dial hue slider events
        self.dial_hue.valueChanged.connect(self.callback_filter_update)
        # pause video while position slider is being moved
        self.slider_video.sliderPressed.connect(self.pause_video)
        # resume after slider is released
        self.slider_video.sliderReleased.connect(
            self.move_video_to_slider_position
        )
        self.statusbar.showMessage("No file selected")

        # timer for video playback
        self.timer = QTimer()
        # call funtion to display a new video frame after timeout time
        self.timer.timeout.connect(self.trigger_update_frame)

        # video is playing status flag
        self.is_playing: bool = False
        self.export_process: Optional[multiprocessing.Process] = None
        # dataclass object for storing video related values
        self.video_data = DCVideoData()
        self.load_status: TypeLoadStatus = TypeLoadStatus.ok

    def resizeEvent(self, event) -> None:
        """
        Callback function called when window is resized.
        :param event:
        :return: None
        """
        pass
        # resize_handler()

    def select_video_file(self) -> None:
        """
        Callback function called when btn is pressed to select a new video.
        The purpose is to load a new video and store all video values
        like fps, frame count, etc in data object.
        :return: None
        """

        # get input file filename
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video",
            "",
            "Video Files (*.mp4 *.avi *.mov)",
        )
        # if a file is selected
        if file_name:
            # store input path in data object
            self.video_data.input_path = file_name
            # call function to load the video and its parameters
            self.video_data, self.load_status = file_loader(self.video_data)
            # process status returned from video load
            self.digest_load_status(self.load_status)

    def reset_values_for_new_video(self) -> None:
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
        # set text fro fps and reoslution labels
        self.label_fps.setText(f"FPS: {self.video_data.fps}")
        self.label_resolution.setText(
            f"Resolution: {self.video_data.frame_size[0]} x {self.video_data.frame_size[1]} px."
        )
        # get only first frame for display in video area
        # as video placeholder until video is started
        ret, frame = self.video_data.cap.read()
        # store as last playing frame
        self.video_data.last_playing_frame = frame
        # store also as first frame
        self.video_data.first_frame = frame
        # apply filter values from sliders
        frame = self.get_filter_values_and_apply_to_frame(frame)
        # put first filtered frame in video ui place.
        self.update_video_in_ui(frame)

    def reset_app_values_invalid_file(self) -> None:
        """
        Function called when video file is invalid.
        Set the ui and app values for the invalid file.
        Like reset FPS and Resoulution labels and qstatus text.
        :return: None
        """
        self.statusbar.showMessage("Invalid video file.")
        self.slider_video.setRange(0, 0)
        self.slider_video.setValue(0)
        self.slider_video.setEnabled(True)
        self.is_playing = False
        self.btn_play_pause.setText("Play")
        self.label_time.setText("00:00 / 00:00")
        self.label_video.setText("Invalid video file")
        self.label_fps.setText(f"FPS: -")
        self.label_resolution.setText(f"Resolution: -")
        self.video_data.cap = None
        self.video_data.fps = None
        self.video_data.total_time = None
        self.video_data.total_frames = None
        self.video_data.current_time = None
        self.video_data.first_frame = None
        self.video_data.last_playing_frame = None
        self.video_data.frame_size = None

    def digest_load_status(self, status: TypeLoadStatus) -> None:
        """
        Function to digest returned video load status.
        :param status: the video load response status
        :return: None
        """
        # show dialog if error
        if status is TypeLoadStatus.error:
            # show msg with file name that could not be loaded
            # ### messages should be built in an extra function
            msg = f"Error: Could not open video file {self.video_data.input_path}. It may be corrupted or missing."
            self.show_user_dialog(
                TypeDialog.error,
                "File Error",
                msg,
            )
            # delete path from dataclass object
            self.video_data.input_path = None
            # reset app and ui values since video file is not valid
            self.reset_app_values_invalid_file()
        # if video was loaded ok
        elif status is TypeLoadStatus.ok:
            # set app and ui values for new video
            self.reset_values_for_new_video()
            # show msg with some file information
            # messages should be built in an extra function
            msg = f"""
            Video loaded successfully!
            
            FPS: {self.video_data.fps}
            Resolution: {self.video_data.frame_size[0]} x {self.video_data.frame_size[1]} px.
            Duration: {self.video_data.total_time} sec.
            Nr. of Frames: {self.video_data.total_frames}
            """

            if self.video_data.video_status is TypeVideoTypeStatus.video_ok:
                self.show_user_dialog(TypeDialog.info, "Video Loaded", msg)

            elif (
                self.video_data.video_status
                is TypeVideoTypeStatus.video_too_short
            ):
                msg += """\nWarning: Video is very short!"""
                self.show_user_dialog(TypeDialog.warning, "Video Loaded", msg)

            # elif self.video_data.video_status is something_else: ....

    def show_user_dialog(
        self,
        dialog_type: TypeDialog,
        title: Optional[str] = None,
        message: Optional[str] = None,
    ) -> None:
        """
        Function that triggers an ui dialog.
        :param dialog_type: type of dialog to trigger
        :param title: dialog title
        :param message: dialog msg
        :return: None
        """

        if dialog_type is TypeDialog.info:
            QMessageBox.information(self, title, message)
        elif dialog_type is TypeDialog.error:
            QMessageBox.critical(self, title, message)
        elif dialog_type is TypeDialog.warning:
            QMessageBox.warning(self, title, message)

    def play_pause_video(self) -> None:
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

    def pause_video(self) -> None:
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

    def stop_video(self) -> None:
        """
        Stop the video.
        Reset some values to start again.
        :return: None
        """

        # if there is a video
        if self.video_data.cap:
            # stop the timer (This timer calls a function for
            # updating video frames)
            self.timer.stop()
            # set property identifier to 0. In this case:
            # CAP_PROP_POS_FRAMES: 0-based index of the frame
            # to be decoded/captured next. (from docs)
            self.video_data.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            # set flag state to not playing
            self.is_playing = False
            # set btn text accordingly
            self.btn_play_pause.setText("Play")
            # reset the time to 00:00 since video was paused
            self.update_time_label(0)
            # reset the slider to o since video was paused
            self.slider_video.setValue(0)
            #  alternative behaviour #
            # Display first frame again
            # self.update_video_in_ui(self.video_data.first_frame)
            # set last shown frame to first video frame
            # self.video_data.last_playing_frame = self.video_data.first_frame

    def update_time_label(self, current_frame) -> None:
        """
        Function called to change the time label shown in the ui
        depending on current video frame
        :param current_frame:
        :return: None
        """

        # get current seconds calculated from fps
        # (frame per second) and current_frame
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
        # store video time values in data object
        self.video_data.total_time = total_time
        self.video_data.current_time = current_time

    def move_video_to_slider_position(self) -> None:
        """
        Move the video accordingly to slider position
        :return: None
        """
        # if there is a video
        if self.video_data.cap:
            # set CAP_PROP_POS_FRAMES property to slider value
            self.video_data.cap.set(
                cv2.CAP_PROP_POS_FRAMES,
                self.slider_video.value(),
            )
            # update frame shown in ui according app state and filter values
            self.trigger_update_frame()
            # resume video playback (video is paused with
            # callback when slider is clicked)
            self.play_pause_video()

    def update_video_in_ui(self, frame) -> None:
        """
        Function used for displaying a single image in the ui.
        The frame is a 3-dim array representing a single image frame from video.
        The image is diplayed in a QPixmap element.
        :param frame:
        :return:
        """

        # get the shape of the numpy array
        height, width, channel = frame.shape
        # bytes_per_line = width×bytes pro pixel (3, rgb)
        bytes_per_line = 3 * width
        # the QImage class provides a hardware-independent image representation
        # that allows direct access to the pixel data. (from docs)
        # OpenCV reads images in BGR (Blue, Green, Red) format by default. (from docs)
        q_img = QImage(
            frame.data,  # Python buffer object pointing to the start of the array’s data.
            width,
            height,
            bytes_per_line,
            QImage.Format.Format_BGR888,
        )  # Format_RGB888 ?

        # scale the image to a height of 300
        # better would be to scale in proportion of container size.
        pixmap = QPixmap.fromImage(q_img).scaledToHeight(400)

        # pixmap = QPixmap.fromImage(q_img).scaledToHeight(
        #     (self.label_video.height())
        # )

        # set the image pixels as content in the ui
        self.label_video.setPixmap(pixmap)

        # if video is playing
        if self.is_playing:
            # update video position bar
            current_frame = int(
                self.video_data.cap.get(cv2.CAP_PROP_POS_FRAMES)
            )
            self.slider_video.setValue(current_frame)
            # update the time shown in ui
            self.update_time_label(current_frame)

    def callback_filter_update(self) -> None:
        """
        Callback function called when filter value change.
        Do frame update only if video is not playing.
        If video is playing, then update will happen automatically
        when self.timer times out and function trigger_update_frame is called.
        :return:
        """
        # if no video capture (cv2.VideoCapture) then do nothing and return
        if self.video_data.cap is None:
            return
        # if video is playing, then do nothing. Return
        # frame with new filter values will be automatically updated
        # when self.timer times out
        if self.video_data.last_playing_frame is None:
            return

        if self.is_playing:
            return

        # Take the last frame displayed and apply the filters and update
        # the ui to show the filtered frame.
        # filter last frame
        frame = self.get_filter_values_and_apply_to_frame(
            self.video_data.last_playing_frame
        )
        # pass filterd frame to ui update function
        self.update_video_in_ui(frame)

    def trigger_update_frame(self) -> None:
        """
        Funtion called by self.timer timeout to update video frame.
        Timeout is calculated using fps: 1000 / self.video_data.fps
        :return: None
        """
        # if no video capture (cv2.VideoCapture) then do nothing and return
        if self.video_data.cap is None:
            return

        # Get next frame.
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
        self.video_data.last_playing_frame = frame
        # filter last frame
        frame = self.get_filter_values_and_apply_to_frame(frame)
        # pass filterd frame to ui update function
        self.update_video_in_ui(frame)

    def get_filter_values_from_widgets(
        self,
    ) -> DCFiltersParams:
        """
        Function that read current values from filter sliders.
        :return: DCFiltersParams, Dataclass object with all filter values.
        """

        # read filter sliders and put values in dataclass
        dc_filter_params = DCFiltersParams(
            blur_strength=self.slider_blur.value(),
            canny_threshold=self.slider_canny.value(),
            sepia_strength=self.slider_sepia.value(),
            brightness_strength=self.slider_brightness.value(),
            saturation_strength=self.slider_saturation.value(),
            sharpen_strength=self.slider_sharpen.value(),
            hue_value=self.dial_hue.value(),
        )
        # return
        return dc_filter_params

    def get_filter_values_and_apply_to_frame(
        self, frame: npt.NDArray
    ) -> npt.NDArray:
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

    def export_video_to_file(self) -> None:
        """
        Callback function called when export btn is pressed.
        Gets the values needed for the export process and calls
        the function to start the subprocess.
        :return:
        """

        # if btn is pressed but we dont have a video file loaded
        # input_path that was set when we loaded the
        # last file (fnc select_video_file).
        if not self.video_data.input_path:
            # Show an ui warning message to user and return
            self.show_user_dialog(
                TypeDialog.warning,
                "No Video Selected",
                "Please select a video first.",
            )
            return

        # get the output filename.
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Processed Video",
            "",
            "MP4 Files (*.mp4)",
        )

        if not save_path:
            return

        # get current filter values from sliders
        dc_filter_params = self.get_filter_values_from_widgets()

        # Put video parameters, filter values and output
        # path together in data object
        dc_export_params_data_for_proc = DCVideoExportParams(
            filter_params=dc_filter_params,
            output_path=save_path,
            input_path=self.video_data.input_path,
        )

        # pass data object with all parameters to function
        # for starting process in background
        self.export_process = export_process(dc_export_params_data_for_proc)

        # Display message to user that export process is
        # running in background
        self.show_user_dialog(
            TypeDialog.info,
            "Export Started",
            "Video export is running in the background.",
        )

    def closeEvent(self, event) -> None:
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
