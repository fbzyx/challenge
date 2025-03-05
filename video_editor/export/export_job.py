import cv2
import numpy as np
import multiprocessing

from ..filter.filter_apply import apply_filters


def video_exporter_job(
    video_path,
    save_path,
    fps,
    frame_size,
    blur_value,
    canny_value,
    sepia_value,
    brightness_value,
    saturation_value,
    sharpen_value,
):
    """Background process to apply filters and export the video."""
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(save_path, fourcc, fps, frame_size)

    sepia_matrix = np.array(
        [[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]]
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Apply filters
        frame = apply_filters(
            frame,
            blur_value,
            canny_value,
            sepia_value,
            brightness_value,
            saturation_value,
            sharpen_value,
        )

        out.write(frame)

    cap.release()
    out.release()
