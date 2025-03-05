from filters.blur import blur_apply
from filters.brightness import brightness_apply
from filters.canny import canny_apply
from filters.saturation import saturation_apply
from filters.sepia import sepia_apply
from filters.sharpen import sharpen_apply


def apply_filters(
    frame,
    blur_strength,
    canny_threshold,
    sepia_strength,
    brightness_strength,
    saturation_strength,
    sharpen_strength,
):
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

    frame = blur_apply(frame, blur_strength)
    frame = canny_apply(frame, canny_threshold)
    frame = brightness_apply(frame, brightness_strength)
    frame = saturation_apply(frame, saturation_strength)
    frame = sepia_apply(frame, sepia_strength)
    frame = sharpen_apply(frame, sharpen_strength)

    return frame
