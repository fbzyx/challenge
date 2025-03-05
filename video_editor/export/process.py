import multiprocessing
from export.export import video_exporter_func
from models.dc_video import DCVideoExportParams
from typing import Union


def export_process(
    export_params_data: DCVideoExportParams,
) -> Union[multiprocessing.Process, None]:
    if not export_params_data.output_path:
        return None

    # Run export in background process
    export_process = multiprocessing.Process(
        target=video_exporter_func,
        args=(export_params_data,),
    )
    export_process.start()

    return export_process
