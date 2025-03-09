import multiprocessing
from typing import Union

from models.dc_video import DCVideoExportParams

from export.export import video_exporter_func


def export_process(
    export_params_data: DCVideoExportParams,
) -> Union[multiprocessing.Process, None]:
    """
    Function that is used to start a background process with multiprocessing.
    A function that exports a filtered video is started in the background.
    :param export_params_data:
    :return: multiprocessing.Process instance if worker start succefully, otherwise None.
    """
    # if no output_path defined, then return None
    if not export_params_data.output_path:
        return None

    # Run export in background process
    export_process = multiprocessing.Process(
        target=video_exporter_func,
        args=(export_params_data,),
    )
    # start background task
    export_process.start()

    # return process instance
    return export_process
