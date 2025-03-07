import unittest
import numpy as np
from filter.filters.brightness import brightness_apply


class TestBrightnessApply(unittest.TestCase):
    """
    Test for Brightness filter
    """

    def setUp(self):
        # Create a dummy image (gray image of size 100x100 with 3 color channels)
        self.image = np.full((100, 100, 3), 128, dtype=np.uint8)

    def test_brightness_apply_no_change(self):
        # if value is 0, the function should return the same image
        result = brightness_apply(self.image, 0)
        np.testing.assert_array_equal(result, self.image)

    def test_brightness_apply_increase(self):
        # if value > 0, the function should increase brightness
        value = 50
        result = brightness_apply(self.image, value)
        expected = np.clip(self.image.astype(np.int16) + value, 0, 255).astype(np.uint8)
        np.testing.assert_array_equal(result, expected)

    def test_brightness_apply_decrease(self):
        # if value < 0, the function should decrease brightness
        value = -50
        result = brightness_apply(self.image, value)
        expected = np.clip(self.image.astype(np.int16) + value, 0, 255).astype(np.uint8)
        np.testing.assert_array_equal(result, expected)

    def test_brightness_apply_max_limit(self):
        # test if brightness increase respects the max limit (255)
        value = 200
        result = brightness_apply(self.image, value)
        expected = np.full(
            (100, 100, 3), 255, dtype=np.uint8
        )  # all values should be capped at 255
        np.testing.assert_array_equal(result, expected)

    def test_brightness_apply_min_limit(self):
        # test if brightness decrease respects the min limit (0)
        value = -200
        result = brightness_apply(self.image, value)
        expected = np.full(
            (100, 100, 3), 0, dtype=np.uint8
        )  # all values should be capped at 0
        np.testing.assert_array_equal(result, expected)


if __name__ == "__main__":
    unittest.main()
