import cv2
import numpy as np


def hue_apply(frame, hue_shift):
    """
    Adjusts the hue of an image.
    :param frame: Input image (BGR format).
    :param hue_shift: Amount to shift the hue (range: -180 to 180).
    :return: Hue-adjusted image.
    """
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)

    # Add hue shift (wrap-around at 180 degrees)
    hsv[:, :, 0] = (hsv[:, :, 0] + hue_shift) % 180

    # Convert back to BGR
    frame = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    return frame
