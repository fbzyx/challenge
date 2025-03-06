import unittest
import numpy as np
from filter.filters.canny import canny_apply


class TestCannyApply(unittest.TestCase):
    def setUp(self):
        # Create a dummy grayscale image (size 100x100)
        self.image = np.full((100, 100, 3), 128, dtype=np.uint8)

    def test_canny_apply_no_edges(self):
        # If value is 0, the function should return the same image
        result = canny_apply(self.image, 0)
        np.testing.assert_array_equal(result, self.image)

    def test_canny_apply_with_edges(self):
        # If value > 0, edges should be detected and converted to BGR
        value = 100
        result = canny_apply(self.image, value)
        self.assertEqual(result.shape, self.image.shape)
        self.assertEqual(result.dtype, np.uint8)

        # Ensure it's not identical to the original (edges detected)
        self.assertFalse(np.array_equal(result, self.image))

    def test_canny_apply_high_threshold(self):
        # Test with a high edge detection threshold
        value = 255
        result = canny_apply(self.image, value)
        self.assertEqual(result.shape, self.image.shape)
        self.assertEqual(result.dtype, np.uint8)

    def test_canny_apply_low_threshold(self):
        # Test with a low edge detection threshold
        value = 10
        result = canny_apply(self.image, value)
        self.assertEqual(result.shape, self.image.shape)
        self.assertEqual(result.dtype, np.uint8)


if __name__ == "__main__":
    unittest.main()
