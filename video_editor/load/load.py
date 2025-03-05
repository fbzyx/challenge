import cv2
from models.dc_video import DCVideoData


def file_loader(video_data_params: DCVideoData) -> DCVideoData:
    video_data_params.cap = cv2.VideoCapture(video_data_params.input_path)
    video_data_params.fps = int(video_data_params.cap.get(cv2.CAP_PROP_FPS))
    video_data_params.total_frames = int(
        video_data_params.cap.get(cv2.CAP_PROP_FRAME_COUNT)
    )
    frame_width = int(video_data_params.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video_data_params.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    video_data_params.frame_size = (frame_width, frame_height)

    return video_data_params
