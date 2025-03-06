import unittest
import cv2
import numpy as np
from filter.filters.saturation import saturation_apply


class TestSaturationApply(unittest.TestCase):
    def setUp(self):
        # Create a dummy image (BGR image of size 100x100 with a mid-tone color)
        self.image = np.full((100, 100, 3), (100, 150, 200), dtype=np.uint8)

    def test_saturation_apply_no_change(self):
        # If value is 0, the function should return the same image
        result = saturation_apply(self.image, 0)
        np.testing.assert_array_equal(result, self.image)

    def test_saturation_apply_increase(self):
        # If value > 0, saturation should increase
        value = 50
        result = saturation_apply(self.image, value)
        self.assertEqual(result.shape, self.image.shape)
        self.assertFalse(np.array_equal(result, self.image))  # Ensure the image changed

    def test_saturation_apply_decrease(self):
        # If value < 0, saturation should decrease
        value = -50
        result = saturation_apply(self.image, value)
        self.assertEqual(result.shape, self.image.shape)
        self.assertFalse(np.array_equal(result, self.image))  # Ensure the image changed

    def test_saturation_apply_max_limit(self):
        # Test if saturation increase respects the max limit (255)
        value = 200
        result = saturation_apply(self.image, value)
        hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
        self.assertTrue(
            np.all(hsv[:, :, 1] <= 255)
        )  # Ensure saturation does not exceed 255

    def test_saturation_apply_min_limit(self):
        # Test if saturation decrease respects the min limit (0)
        value = -200
        result = saturation_apply(self.image, value)
        hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
        self.assertTrue(
            np.all(hsv[:, :, 1] >= 0)
        )  # Ensure saturation does not go below 0


if __name__ == "__main__":
    unittest.main()
