import numpy.typing as npt
from models.dc_video import DCFiltersParams

from filter.filters.blur import blur_apply
from filter.filters.brightness import brightness_apply
from filter.filters.canny import canny_apply
from filter.filters.saturation import saturation_apply
from filter.filters.sepia import sepia_apply
from filter.filters.sharpen import sharpen_apply


def get_filtered_frame(
    frame: npt.NDArray, filter_data_params: DCFiltersParams
) -> npt.NDArray:
    """
    Function called to filter a given frame with the given values.

    Recommended Filter Order:

    - Blur: Smooths noise, making edge detection more stable.
    - Canny (Edge Detection): Should be applied before any color
      changes (like sepia, brightness, or saturation) to detect edges accurately.
    - Sharpen: Enhances details; best applied after blurring to bring back clarity.
    - Brightness: Adjusts overall intensity; should be applied before color-based changes.
    - Saturation: Adjusts color vibrancy, depending on brightness.
    - Sepia: Converts the image to a warm-toned style, best applied last to
      avoid interference from other filters.

    :param frame: the frame to filer.
    :param filter_data_params: the values for each filter from the ui sliders.
    :return: filtered frame.
    """

    # filter the frame respecting the filter order
    frame = blur_apply(frame, filter_data_params.blur_strength)
    frame = canny_apply(frame, filter_data_params.canny_threshold)
    frame = sharpen_apply(frame, filter_data_params.sharpen_strength)
    frame = brightness_apply(frame, filter_data_params.brightness_strength)
    frame = saturation_apply(frame, filter_data_params.saturation_strength)
    frame = sepia_apply(frame, filter_data_params.sepia_strength)

    return frame
