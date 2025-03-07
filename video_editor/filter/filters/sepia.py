import cv2
import numpy as np
import numpy.typing as npt

sepia_matrix = np.array(
    [[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]]
)


def sepia_apply(frame: npt.NDArray, value) -> npt.NDArray:
    """
    Apply a sepia filter with sepia matrix.
    :param frame: frame to filter
    :param value: slider value
    :return: filtered frame
    """
    if value > 0:
        sepia_filter = (value / 100.0) * sepia_matrix + (1 - value / 100.0) * np.eye(3)
        frame = cv2.transform(frame, sepia_filter)
        frame = np.clip(frame, 0, 255).astype(np.uint8)

    return frame
