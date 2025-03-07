import numpy as np
import numpy.typing as npt


def brightness_apply(frame: npt.NDArray, value) -> npt.NDArray:
    """
    Increase or decrease brightness.
    :param frame: frame to filter
    :param value: slider value
    :return: filtered frame
    """
    if value != 0:
        # clip (limit) the values in an array -> increase or decrease matrix values depending of slider value.
        frame = np.clip(frame.astype(np.int16) + value, 0, 255).astype(np.uint8)
    return frame
