import unittest
from unittest.mock import MagicMock, patch

import cv2
from models.dc_video import DCVideoData
from models.type_status import (
    TypeLoadStatus,
    TypeVideoTypeStatus,
)

from load.load import file_loader


def side_effect_func_open_true() -> bool:
    """
    Return for isOpened true
    :return: True
    """
    return True


def side_effect_func_open_false() -> bool:
    """
    Return for isOpened false
    :return: False
    """
    return False


def side_effect_func_get_prop(propid) -> int:
    """
    Return value of fake opencv property
    :param propid: cv2 property
    :return: property int value
    """
    properties = {
        cv2.CAP_PROP_FPS: 30,
        cv2.CAP_PROP_FRAME_COUNT: 1000,
        cv2.CAP_PROP_FRAME_WIDTH: 1920,
        cv2.CAP_PROP_FRAME_HEIGHT: 1080,
    }

    return properties.get(propid)


class TestFileLoader(unittest.TestCase):
    @patch.object(
        cv2.VideoCapture,
        "isOpened",
        side_effect=side_effect_func_open_true,
    )
    @patch.object(
        cv2.VideoCapture,
        "get",
        side_effect=side_effect_func_get_prop,
    )
    def test_file_loader_open_video(self, mock_cv2_cap, mock_cv2_cap_get):
        # set up mock return values for get() method
        # mock_cv2_cap.get.return_value = {
        #     cv2.CAP_PROP_FPS: 30,
        #     cv2.CAP_PROP_FRAME_COUNT: 1000,
        #     cv2.CAP_PROP_FRAME_WIDTH: 1920,
        #     cv2.CAP_PROP_FRAME_HEIGHT: 1080,
        # }

        # mock_cv2_cap.return_value = self.side_effect_func
        # mock_cv2_cap.get = MagicMock(side_effect=self.side_effect_func)
        # mock_cv2_cap.isOpened.return_value = True

        # create DCVideoData object
        video_data_params = DCVideoData(input_path="test_video.mp4")

        # call the function
        result, status = file_loader(video_data_params)

        # check the results
        self.assertEqual(
            result.fps,
            side_effect_func_get_prop(cv2.CAP_PROP_FPS),
        )
        self.assertEqual(
            result.total_frames,
            side_effect_func_get_prop(cv2.CAP_PROP_FRAME_COUNT),
        )
        self.assertEqual(
            result.video_status,
            TypeVideoTypeStatus.video_ok,
        )
        self.assertEqual(status, TypeLoadStatus.ok)
        self.assertEqual(
            result.frame_size,
            (
                side_effect_func_get_prop(cv2.CAP_PROP_FRAME_WIDTH),
                side_effect_func_get_prop(cv2.CAP_PROP_FRAME_HEIGHT),
            ),
        )

    @patch.object(
        cv2.VideoCapture,
        "isOpened",
        side_effect=side_effect_func_open_false,
    )
    @patch.object(
        cv2.VideoCapture,
        "get",
        side_effect=side_effect_func_get_prop,
    )
    def test_file_loader_not_open_video(self, mock_cv2_cap, mock_cv2_cap_get):
        # create DCVideoData object
        video_data_params = DCVideoData(input_path="test_video.mp4")

        # call the function
        result, status = file_loader(video_data_params)

        # check the results
        self.assertNotEqual(
            result.fps,
            side_effect_func_get_prop(cv2.CAP_PROP_FPS),
        )
        self.assertNotEqual(
            result.total_frames,
            side_effect_func_get_prop(cv2.CAP_PROP_FRAME_COUNT),
        )
        self.assertEqual(
            result.video_status,
            TypeVideoTypeStatus.video_undefined,
        )
        self.assertEqual(status, TypeLoadStatus.error)
        self.assertNotEqual(
            result.frame_size,
            (
                side_effect_func_get_prop(cv2.CAP_PROP_FRAME_WIDTH),
                side_effect_func_get_prop(cv2.CAP_PROP_FRAME_HEIGHT),
            ),
        )


if __name__ == "__main__":
    unittest.main()
