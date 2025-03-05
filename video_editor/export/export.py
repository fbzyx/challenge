import cv2
import numpy as np
import multiprocessing

from filter.filter import get_filtered_frame
from models.dc_video import DCVideoExportParams


def video_exporter_func(export_params_data: DCVideoExportParams) -> None:
    """Background process to apply filters and export the video."""

    cap = cv2.VideoCapture(export_params_data.video_data.input_path)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    out = cv2.VideoWriter(
        export_params_data.output_path,
        fourcc,
        export_params_data.video_data.fps,
        export_params_data.video_data.frame_size,
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Apply filters
        frame = get_filtered_frame(frame, export_params_data.filter_params)

        out.write(frame)

    cap.release()
    out.release()
