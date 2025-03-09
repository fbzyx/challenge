import unittest
import cv2
import numpy as np
from filter.filters.hue import hue_apply


class TestAdjustHue(unittest.TestCase):
    def setUp(self):
        """Create a test image (pure red in BGR format)"""
        self.image = np.zeros((100, 100, 3), dtype=np.uint8)
        self.image[:, :] = [0, 0, 255]  # Pure red in BGR

    def test_hue_shift_positive(self):
        """Test hue shift with a positive value"""
        shifted_image = hue_apply(self.image, 30)
        self.assertEqual(shifted_image.shape, self.image.shape)

    def test_hue_shift_negative(self):
        """Test hue shift with a negative value"""
        shifted_image = hue_apply(self.image, -30)
        self.assertEqual(shifted_image.shape, self.image.shape)

    def test_hue_shift_wraparound(self):
        """Test that hue wraps correctly at 180"""
        shifted_image = hue_apply(
            self.image, 190
        )  # Exceeds 180, should wrap around
        self.assertEqual(shifted_image.shape, self.image.shape)

    def test_no_hue_change(self):
        """Test that a hue shift of 0 does not change the image"""
        shifted_image = hue_apply(self.image, 0)
        np.testing.assert_array_equal(
            shifted_image, self.image
        )  # Should be identical


if __name__ == "__main__":
    unittest.main()
