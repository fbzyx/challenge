import multiprocessing
from export_job import video_exporter_job

def export_video_process(self, output_path):

    if not output_path:
        return

    # Run export in background process
    self.export_process = multiprocessing.Process(
        target=video_exporter_job,
        args=(
            self.video_path,
            output_path,
            self.fps,
            (self.frame_width, self.frame_height),
            self.slider_blur.value(),
            self.slider_canny.value(),
            self.slider_sepia.value(),
            self.slider_brightness.value(),
            self.slider_saturation.value(),
            self.slider_sharpen.value(),
        ),
    )
    self.export_process.start()
