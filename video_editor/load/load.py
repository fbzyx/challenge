from typing import Tuple

import cv2
from models.dc_video import DCVideoData
from models.type_status import (
    TypeLoadStatus,
    TypeVideoTypeStatus,
)


def set_video_status(
    video_data_params: DCVideoData,
    load_status: TypeLoadStatus,
) -> DCVideoData:
    """
    Set the video status flag for videos that are too short or have too small framesize.
    Further video checks could be done here..

    :param video_data_params: video data object with values for newly imported video.
    :param load_status: the file loading status (ok or error).
    :return: DCVideoData with video status updated
    """
    # check values for videos that are too shorts, have very small framesizes, etc..
    # and set the video_status flag
    if load_status is TypeLoadStatus.ok:
        # check duration
        if video_data_params.total_time < 1:
            # if video is less than one sec, then add video_too_short flag
            video_data_params.video_status = TypeVideoTypeStatus.video_too_short

        # if video has a very small framesize, then add video_size_framesize_small flag
        elif video_data_params.frame_size[0] < 10:
            video_data_params.video_status = (
                TypeVideoTypeStatus.video_size_framesize_small
            )
        elif video_data_params.frame_size[1] < 10:
            video_data_params.video_status = (
                TypeVideoTypeStatus.video_size_framesize_small
            )
        # other cases ...
        # elif ..:
        #     pass
        # elif ..:
        #     pass
    # if file could not be loaded, then video status is undefined..
    else:
        video_data_params.video_status = TypeVideoTypeStatus.video_undefined

    return video_data_params


def file_loader(
    video_data_params: DCVideoData,
) -> Tuple[DCVideoData, TypeLoadStatus]:
    """
    Load file from video_data_params.input_path and check if file can be opened.
    If the file cannot be opened, it is probably damaged or not supported.
    :param video_data_params: Data object to store the video related values.
    :return: Tuple[DCVideoData, TypeLoadStatus]. Dataclass object with video values, file load status.
    """

    # load file
    video_data_params.cap = cv2.VideoCapture(video_data_params.input_path)

    # check if file can be opened
    if not video_data_params.cap.isOpened():
        # if not, then we have an error, set video load status to error
        load_status = TypeLoadStatus.error
        video_data_params.cap.release()
        video_data_params.cap = None
    else:
        # if ok, then set video status to ok
        load_status = TypeLoadStatus.ok
        video_data_params.video_status = TypeVideoTypeStatus.video_ok
        # read and store basic video data in data object
        # fps
        video_data_params.fps = int(video_data_params.cap.get(cv2.CAP_PROP_FPS))
        # total frames
        video_data_params.total_frames = int(
            video_data_params.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        )
        # framesize
        frame_width = int(video_data_params.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video_data_params.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        video_data_params.frame_size = (
            frame_width,
            frame_height,
        )
        # duration: total frames / fps
        video_data_params.total_time = (
            video_data_params.total_frames / video_data_params.fps
        )

    # pass video values to function to check if all is ok and get video status flag
    # maybe video is very short, small framesize, etc..
    video_data_params = set_video_status(video_data_params, load_status)

    return video_data_params, load_status
