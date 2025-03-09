from dataclasses import dataclass, field
from typing import Optional, Tuple

import numpy.typing as npt
from cv2 import VideoCapture

from models.type_status import TypeVideoTypeStatus


@dataclass
class DCVideoData:
    fps: Optional[int] = None
    frame_size: Optional[Tuple[int, int]] = None
    total_frames: Optional[int] = None
    input_path: Optional[str] = None
    cap: Optional[VideoCapture] = None
    last_playing_frame: Optional[npt.NDArray] = None
    first_frame: Optional[npt.NDArray] = None
    total_time: Optional[int] = None
    current_time: Optional[int] = None
    video_status: Optional[TypeVideoTypeStatus] = (
        TypeVideoTypeStatus.video_undefined
    )


@dataclass
class DCFiltersParams:
    blur_strength: Optional[int] = None
    canny_threshold: Optional[int] = None
    sepia_strength: Optional[int] = None
    brightness_strength: Optional[int] = None
    saturation_strength: Optional[int] = None
    sharpen_strength: Optional[int] = None


@dataclass
class DCVideoExportParams:
    filter_params: Optional[DCFiltersParams] = None
    output_path: Optional[str] = None
    input_path: Optional[str] = None
