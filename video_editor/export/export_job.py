import cv2
import numpy as np
import multiprocessing

from filter.filter_apply import apply_filters


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
