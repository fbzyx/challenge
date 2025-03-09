import cv2
from filter.filter_frame import get_filtered_frame
from models.dc_video import DCVideoExportParams


def video_exporter_func(
    export_params_data: DCVideoExportParams,
) -> None:
    """
    Worker function called to export a video.
    The video from input_path is filtered with given params and saved in output_path video.
    :param export_params_data: Dataclass object with video parameters and filter values.
    :return:
    """

    # get video using input_path from data object
    cap = cv2.VideoCapture(export_params_data.input_path)
    # 4-character code of codec used to compress the frames (mp4 format)
    # *"mp4v" -> m,p,4,v
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    # get video data, also possible to get them from DCVideoExportParams.video_data
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (frame_width, frame_height)

    # video output with mp4 format, output path, fps and frame size (tuple)
    out = cv2.VideoWriter(
        export_params_data.output_path,
        fourcc,
        fps,
        frame_size,
    )

    # iterate until nothing more to read
    while True:
        ret, frame = cap.read()
        # nothing more to read
        if not ret:
            break

        # apply filters, pass filter values as parameter
        frame = get_filtered_frame(frame, export_params_data.filter_params)
        # write
        out.write(frame)

    # at the end release both files (original video and new video)
    cap.release()
    out.release()
