import multiprocessing
from export.export_job import video_exporter_job


def export_video_process(
    video_path,
    output_path,
    fps,
    frame_size,
    blur_strength,
    canny_threshold,
    sepia_strength,
    brightness_strength,
    saturation_strength,
    sharpen_strength,
):
    if not output_path:
        return

    # Run export in background process
    export_process = multiprocessing.Process(
        target=video_exporter_job,
        args=(
            video_path,
            output_path,
            fps,
            frame_size,
            blur_strength,
            canny_threshold,
            sepia_strength,
            brightness_strength,
            saturation_strength,
            sharpen_strength,
        ),
    )
    export_process.start()
