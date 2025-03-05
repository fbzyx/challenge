import cv2
import numpy as np


def blur_apply(frame, value):
    if value > 0:
        frame = cv2.GaussianBlur(frame, (2 * value + 1, 2 * value + 1), 0)
    return frame
