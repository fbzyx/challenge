import unittest

import cv2
import numpy as np
from models.dc_video import DCFiltersParams

from filter.filter_frame import get_filtered_frame


class TestGetFilteredFrame(unittest.TestCase):
    def setUp(self):
        """Create a sample image (frame) for testing."""
        # create a dummy image (image of size 100x100 with 3 color channels)
        shape = (
            100,
            100,
            3,
        )  # 100x100 image with 3 color channels
        # generate random integers between 0 and 255
        self.frame = np.random.randint(0, 256, shape, dtype=np.uint8)

        # define test filter parameters
        self.fake_filter_params = DCFiltersParams(
            blur_strength=10,  # 0-20
            canny_threshold=120,  # 0-255
            sepia_strength=50,  # 0-100
            brightness_strength=30,  # -100-100
            saturation_strength=30,  # -100-100
            sharpen_strength=2,  # 0-5
            hue_value=30,
        )

    def test_get_filtered_frame_output_shape(self):
        """Test if get_filtered_frame keeps the same image shape after applying filters."""
        filtered_frame = get_filtered_frame(self.frame, self.fake_filter_params)

        # output shape should remain the same
        self.assertEqual(self.frame.shape, filtered_frame.shape)

    def test_get_filtered_frame_changes_pixels(self):
        """Test if the frame is actually modified by the filters."""
        filtered_frame = get_filtered_frame(self.frame, self.fake_filter_params)

        # ensure that at least some pixels have changed
        self.assertFalse(np.array_equal(self.frame, filtered_frame))

    def test_get_filtered_frame_valid_pixel_range(self):
        """Test if pixel values remain in the valid range [0, 255] after filtering."""
        filtered_frame = get_filtered_frame(self.frame, self.fake_filter_params)

        # ensure all pixel values are within the correct range
        self.assertTrue(np.all((filtered_frame >= 0) & (filtered_frame <= 255)))


if __name__ == "__main__":
    unittest.main()
