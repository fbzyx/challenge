from dataclasses import dataclass, field
from typing import Tuple, Optional
from cv2 import VideoCapture


@dataclass
class DCVideoData:
    fps: Optional[int] = None
    frame_size: Optional[Tuple[int, int]] = None
    total_frames: Optional[int] = None
    input_path: Optional[str] = None
    cap: Optional[VideoCapture] = None  # cannot pass to subprocess due to not pickeable


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
    video_data: Optional[DCVideoData] = None
    output_path: Optional[str] = None
