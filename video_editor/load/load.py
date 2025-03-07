import cv2
from models.dc_video import DCVideoData
from models.type_status import TypeLoadStatus
from typing import Tuple


def file_loader(video_data_params: DCVideoData) -> Tuple[DCVideoData, TypeLoadStatus]:

    video_data_params.cap = cv2.VideoCapture(video_data_params.input_path)

    if not video_data_params.cap.isOpened():
        status = TypeLoadStatus.error
        video_data_params.cap.release()
        video_data_params.cap = None
    else:
        status = TypeLoadStatus.ok
        video_data_params.fps = int(video_data_params.cap.get(cv2.CAP_PROP_FPS))
        video_data_params.total_frames = int(
            video_data_params.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        )
        frame_width = int(video_data_params.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(video_data_params.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        video_data_params.frame_size = (frame_width, frame_height)
        video_data_params.total_time = (
            video_data_params.total_frames / video_data_params.fps
        )

    return video_data_params, status
