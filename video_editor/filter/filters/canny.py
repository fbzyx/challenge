import cv2
import numpy as np
import numpy.typing as npt


def canny_apply(frame: npt.NDArray, value) -> npt.NDArray:
    """
    Canny filter for edge detection.
    https://docs.opencv.org/4.x/dd/d1a/group__imgproc__feature.html#ga04723e007ed888ddf11d9ba04e2232de
    :param frame: frame to filter
    :param value: slider value
    :return: filtered frame
    """
    if value > 0:
        # value here used for calculating some threshold...
        edges = cv2.Canny(frame, value, value * 2)
        # convert an image from one color space to another.
        frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    return frame
