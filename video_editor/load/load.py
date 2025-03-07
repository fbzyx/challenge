import cv2
from models.dc_video import DCVideoData
from models.type_status import TypeLoadStatus
from typing import Tuple


def file_loader(video_data_params: DCVideoData) -> Tuple[DCVideoData, TypeLoadStatus]:

    status = TypeLoadStatus.ok
    video_data_params.cap = cv2.VideoCapture(video_data_params.input_path)
    video_data_params.fps = int(video_data_params.cap.get(cv2.CAP_PROP_FPS))
    video_data_params.total_frames = int(
        video_data_params.cap.get(cv2.CAP_PROP_FRAME_COUNT)
    )
    frame_width = int(video_data_params.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_data_params.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_data_params.frame_size = (frame_width, frame_height)

    if video_data_params.fps < 1:
        status = TypeLoadStatus.error
    if video_data_params.total_frames < 1:
        status = TypeLoadStatus.error
    if frame_width < 10 or frame_height < 10:
        status = TypeLoadStatus.error

    return (video_data_params, status)
