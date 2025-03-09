import os
import unittest

import cv2
import numpy as np
from models.dc_video import (
    DCFiltersParams,
    DCVideoExportParams,
)

from export.export import video_exporter_func


class TestVideoExporterFunc(unittest.TestCase):
    def setUp(self):
        """Create a temporary video file for testing."""
        self.input_video = "test_input.mp4"
        self.output_video = "test_output.mp4"

        # create a sample video (100x100, 30 FPS, 2 seconds, gray frames)
        frame_size = (100, 100)
        fps = 30
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(self.input_video, fourcc, fps, frame_size)

        # store input frames for comparison
        self.original_frames = []

        for _ in range(60):  # 2 seconds at 30 FPS
            frame = np.ones((100, 100, 3), dtype=np.uint8) * 128  # Gray frame
            self.original_frames.append(frame.copy())
            out.write(frame)

        out.release()

        # define fake filter parameters
        self.fake_filter_params = DCFiltersParams(
            blur_strength=10,  # 0-20
            canny_threshold=120,  # 0-255
            sepia_strength=50,  # 0-100
            brightness_strength=30,  # -100-100
            saturation_strength=30,  # -100-100
            sharpen_strength=2,  # 0-5
            hue_value=30,
        )

        # define export parameters
        self.export_params = DCVideoExportParams(
            input_path=self.input_video,
            output_path=self.output_video,
            filter_params=self.fake_filter_params,
        )

    def test_video_exporter_func(self):
        """
        Test if video_exporter_func correctly processes a video.
        Output video should be different from input video due to the filters.
        """
        video_exporter_func(self.export_params)

        # check if output file is created
        self.assertTrue(os.path.exists(self.output_video))

        # validate the output video
        cap = cv2.VideoCapture(self.output_video)
        self.assertTrue(cap.isOpened())

        # check frame properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.assertEqual(fps, 30)
        self.assertEqual((width, height), (100, 100))

        # check that at least one frame differs due to filters
        frame_differences = 0
        frame_index = 0

        while True:
            ret, output_frame = cap.read()
            if not ret or frame_index >= len(self.original_frames):
                # stop when no more frames to compare
                break

            input_frame = self.original_frames[frame_index]
            if not np.array_equal(input_frame, output_frame):
                frame_differences += 1

            frame_index += 1

        cap.release()

        # ensure that at least one frame is different due to filter application
        self.assertGreater(
            frame_differences,
            0,
            "Filtered video frames should differ from original frames",
        )

    def tearDown(self):
        """Clean up temporary files."""
        if os.path.exists(self.input_video):
            os.remove(self.input_video)
        if os.path.exists(self.output_video):
            os.remove(self.output_video)


if __name__ == "__main__":
    unittest.main()
