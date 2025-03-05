import cv2
import numpy as np


def sharpen_apply(frame, value):
    if value > 0:
        kernel = np.array([[0, -1, 0], [-1, 5 + value, -1], [0, -1, 0]])
        frame = cv2.filter2D(frame, -1, kernel)
    return frame
