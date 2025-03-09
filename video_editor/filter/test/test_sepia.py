import unittest

import numpy as np

from filter.filters.sepia import sepia_apply


class TestSepiaApply(unittest.TestCase):
    """
    Test for sepia filter
    """

    def setUp(self):
        # create a dummy image (BGR image of size 100x100 with a mid-tone color)
        self.image = np.full((100, 100, 3), (100, 150, 200), dtype=np.uint8)

    def test_sepia_apply_no_change(self):
        # if value is 0, the function should return the same image
        result = sepia_apply(self.image, 0)
        np.testing.assert_array_equal(result, self.image)

    def test_sepia_apply_low_intensity(self):
        # if value is small, the change should be subtle
        value = 20
        result = sepia_apply(self.image, value)
        self.assertEqual(result.shape, self.image.shape)
        self.assertFalse(
            np.array_equal(result, self.image)
        )  # Ensure the image changed slightly

    def test_sepia_apply_high_intensity(self):
        # if value is high, the effect should be strong
        value = 100
        result = sepia_apply(self.image, value)
        self.assertEqual(result.shape, self.image.shape)
        self.assertFalse(
            np.array_equal(result, self.image)
        )  # ensure the image changed significantly

    def test_sepia_apply_max_limit(self):
        # ensure values remain within the valid range (0-255)
        value = 100
        result = sepia_apply(self.image, value)
        self.assertTrue(np.all(result >= 0) and np.all(result <= 255))

    def test_sepia_apply_invalid_value(self):
        # if value is negative, it should return the same image
        result = sepia_apply(self.image, -10)
        np.testing.assert_array_equal(result, self.image)


if __name__ == "__main__":
    unittest.main()
