import unittest
from unittest.mock import patch, MagicMock
from models.dc_video import DCVideoData
import cv2

from load.load import file_loader


class TestFileLoader(unittest.TestCase):

    @patch("cv2.VideoCapture")
    def test_file_loader(self, mock_cv2_cap):

        # set up mock return values for get() method
        mock_cv2_cap.return_value = {
            cv2.CAP_PROP_FPS: 30,
            cv2.CAP_PROP_FRAME_COUNT: 1000,
            cv2.CAP_PROP_FRAME_WIDTH: 1920,
            cv2.CAP_PROP_FRAME_HEIGHT: 1080,
        }

        # create DCVideoData object
        video_data_params = DCVideoData(input_path="test_video.mp4")

        # replace the actual VideoCapture with the mock
        video_data_params.cap = mock_cv2_cap

        # act: call the function
        result, status = file_loader(video_data_params)

        # assert: check the results
        self.assertEqual(result.fps, 30)
        self.assertEqual(result.total_frames, 1000)
        self.assertEqual(result.frame_size, (1920, 1080))


if __name__ == "__main__":
    unittest.main()
