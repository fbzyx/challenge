import unittest

import numpy as np

from filter.filters.sharpen import sharpen_apply


class TestSharpenApply(unittest.TestCase):
    """
    Test for sharpen filter
    """

    def setUp(self):
        # create a dummy image (BGR image of size 100x100 with a mid-tone color)
        self.image = np.full((100, 100, 3), (100, 150, 200), dtype=np.uint8)

    def test_sharpen_apply_no_change(self):
        # if value is 0, the function should return the same image
        result = sharpen_apply(self.image, 0)
        np.testing.assert_array_equal(result, self.image)

    def test_sharpen_apply_low_intensity(self):
        # if value is small, the sharpening effect should be subtle
        value = 1
        result = sharpen_apply(self.image, value)
        self.assertEqual(result.shape, self.image.shape)
        self.assertFalse(
            np.array_equal(result, self.image)
        )  # ensure the image changed slightly

    def test_sharpen_apply_high_intensity(self):
        # if value is high, the sharpening effect should be strong
        value = 5
        result = sharpen_apply(self.image, value)
        self.assertEqual(result.shape, self.image.shape)
        self.assertFalse(
            np.array_equal(result, self.image)
        )  # Ensure the image changed significantly

    def test_sharpen_apply_pixel_range(self):
        # Ensure values remain within the valid range (0-255)
        value = 10
        result = sharpen_apply(self.image, value)
        self.assertTrue(np.all(result >= 0) and np.all(result <= 255))

    def test_sharpen_apply_invalid_value(self):
        # if value is negative, it should return the same image
        result = sharpen_apply(self.image, -1)
        np.testing.assert_array_equal(result, self.image)


if __name__ == "__main__":
    unittest.main()
