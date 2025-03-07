import cv2
import numpy as np
import numpy.typing as npt


def saturation_apply(frame: npt.NDArray, value) -> npt.NDArray:
    """
    Change frame saturation.
    :param frame: frame to filter
    :param value: slider value
    :return: filtered frame
    """
    if value != 0:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1].astype(np.int16) + value, 0, 255)
        frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return frame
