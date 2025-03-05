import cv2
from models.dc_video import DCVideoData


def file_loader(video_path: str) -> DCVideoData:
    data = DCVideoData()
    data.cap = cv2.VideoCapture(video_path)
    data.fps = int(data.cap.get(cv2.CAP_PROP_FPS))
    data.total_frames = int(data.cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(data.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(data.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    data.frame_size = (frame_width, frame_height)

    return data
