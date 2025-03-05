import numpy as np


def brightness_apply(frame, value):
    if value != 0:
        frame = np.clip(frame.astype(np.int16) + value, 0, 255).astype(np.uint8)
    return frame
