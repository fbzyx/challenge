from filter.filters.blur import blur_apply
from filter.filters.brightness import brightness_apply
from filter.filters.canny import canny_apply
from filter.filters.saturation import saturation_apply
from filter.filters.sepia import sepia_apply
from filter.filters.sharpen import sharpen_apply
from models.dc_video import DCFiltersParams


def get_filtered_frame(frame, filter_data_params: DCFiltersParams):
    # Apply filters according order

    # Blur
    # Canny(Edge
    # Detection)
    # Brightness & Contrast
    # Adjustments
    # Saturation
    # Adjustment
    # Sepia
    # Effect
    # Sharpening

    frame = blur_apply(frame, filter_data_params.blur_strength)
    frame = canny_apply(frame, filter_data_params.canny_threshold)
    frame = brightness_apply(frame, filter_data_params.brightness_strength)
    frame = saturation_apply(frame, filter_data_params.saturation_strength)
    frame = sepia_apply(frame, filter_data_params.sepia_strength)
    frame = sharpen_apply(frame, filter_data_params.sharpen_strength)

    return frame
