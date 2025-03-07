import cv2
import numpy.typing as npt


def blur_apply(frame: npt.NDArray, value) -> npt.NDArray:
    """
    Blurs an image using a Gaussian filter.
    https://docs.opencv.org/4.x/d4/d86/group__imgproc__filter.html#gae8bdcd9154ed5ca3cbc1766d960f45c1
    :param frame: frame to filter
    :param value: slider value
    :return: filtered frame
    """
    if value > 0:
        # value used to Gaussian kernel size. ksize.width and ksize.height can differ but they both must be positive.
        frame = cv2.GaussianBlur(frame, (2 * value + 1, 2 * value + 1), 0)
    return frame
