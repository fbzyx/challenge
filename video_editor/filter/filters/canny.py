import cv2
import numpy as np


def canny_apply(frame, value):
    if value > 0:
        edges = cv2.Canny(frame, value, value * 2)
        frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    return frame
